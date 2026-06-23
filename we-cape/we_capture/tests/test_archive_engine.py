"""Stage 0.5 — Archive Intelligence Tests"""

import gzip, io, sys, tarfile, tempfile, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from wecape.archive.detector import ArchiveDetector
from wecape.archive.extractor import ArchiveExtractor
from wecape.archive.stage import ArchiveIntelligenceStage

ARCHIVE_CONFIG = {
    'pipeline': {'file_operation': 'copy'},
    'archive_engine': {
        'enabled': True,
        'supported_formats': ['.zip', '.gz', '.tar', '.tar.gz', '.tgz'],
        'extraction': {'preserve_originals': True, 'max_nesting_depth': 3,
                       'isolated_directories': True, 'overwrite_existing': False},
        'size_limits': {'max_single_file_extracted_gb': 10, 'max_total_extracted_gb': 50},
        'partial_downloads': {'markers': ['.crdownload','.part','.download','.tmp','.partial'], 'action': 'quarantine'},
        'encrypted_archives': {'action': 'quarantine'},
        'recursive_container': {'halt_on_detection': True, 'flag_as_corrupted': True},
        'repair': {'attempt_repair': True, 'repair_timeout_seconds': 30},
        'quarantine': {'quarantine_dir': 'QUARANTINE', 'log_quarantine_reason': True},
    },
}

def make_zip(path, files):
    with zipfile.ZipFile(str(path), 'w', zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            zf.writestr(name, data)

def make_tar(path, files):
    with tarfile.open(str(path), 'w') as tf:
        for name, data in files.items():
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))

def make_gz(path, content):
    with gzip.open(str(path), 'wb') as gz:
        gz.write(content)

def make_disguised_gz_as_zip(path, content):
    with gzip.open(str(path), 'wb') as gz:
        gz.write(content)

def test_zip_detected_by_magic(tmp_path):
    f = tmp_path / 'archive.zip'
    make_zip(f, {'test.txt': b'hello'})
    result = ArchiveDetector().detect(f)
    assert result.detected_type == 'zip'
    assert result.detection_method == 'magic_bytes'

def test_mislabeled_gz_as_zip_detected(tmp_path):
    f = tmp_path / 'Unconfirmed_148757.zip'
    make_disguised_gz_as_zip(f, b'real gzip content')
    result = ArchiveDetector().detect(f)
    assert result.detected_type in ('gz', 'tar.gz')
    assert result.extension_mismatch is True

def test_partial_download_crdownload_detected(tmp_path):
    f = tmp_path / 'Unconfirmed 261427.crdownload'
    f.write_bytes(b'\x1f\x8b' + b'\x00' * 100)
    result = ArchiveDetector().detect(f)
    assert result.is_partial_download is True
    assert result.is_archive is False

def test_partial_download_part_detected(tmp_path):
    f = tmp_path / 'media.part'
    f.write_bytes(b'PK\x03\x04' + b'\x00' * 50)
    result = ArchiveDetector().detect(f)
    assert result.is_partial_download is True

def test_recursive_container_cpgz_detected(tmp_path):
    f = tmp_path / 'project.zip.cpgz'
    f.write_bytes(b'\x1f\x8b' + b'\x00' * 50)
    result = ArchiveDetector().detect(f)
    assert result.is_recursive_container is True

def test_7z_detected_as_phase1_format(tmp_path):
    f = tmp_path / 'archive.7z'
    f.write_bytes(b'7z\xbc\xaf\x27\x1c' + b'\x00' * 50)
    result = ArchiveDetector().detect(f)
    assert result.detected_type == '7z'
    assert result.is_phase1_format is True

def test_rar_detected_as_phase1_format(tmp_path):
    f = tmp_path / 'archive.rar'
    f.write_bytes(b'Rar!\x1a\x07\x00' + b'\x00' * 50)
    result = ArchiveDetector().detect(f)
    assert result.is_phase1_format is True

def test_non_archive_returns_not_archive(tmp_path):
    f = tmp_path / 'DJI_0001.mp4'
    f.write_bytes(b'\x00\x00\x00\x18ftyp' + b'\x00' * 50)
    result = ArchiveDetector().detect(f)
    assert result.is_archive is False

def test_zip_extraction_produces_files(tmp_path):
    src = tmp_path / 'test.zip'
    make_zip(src, {'video.mp4': b'fake_video' * 100, 'audio.wav': b'fake_audio' * 50})
    extractor = ArchiveExtractor(ARCHIVE_CONFIG)
    result = extractor.extract(src, tmp_path / 'out', 'zip', depth=0)
    assert result.success is True
    assert len(result.extracted_files) == 2

def test_zip_preserves_original(tmp_path):
    src = tmp_path / 'test.zip'
    make_zip(src, {'clip.mp4': b'data' * 100})
    original_size = src.stat().st_size
    ArchiveExtractor(ARCHIVE_CONFIG).extract(src, tmp_path / 'out', 'zip', depth=0)
    assert src.exists()
    assert src.stat().st_size == original_size

def test_tar_extraction(tmp_path):
    src = tmp_path / 'media.tar'
    make_tar(src, {'DJI_0001.mp4': b'dji_data' * 200})
    result = ArchiveExtractor(ARCHIVE_CONFIG).extract(src, tmp_path / 'out', 'tar', depth=0)
    assert result.success is True

def test_gz_extraction_single_file(tmp_path):
    src = tmp_path / 'export.gz'
    make_gz(src, b'raw content' * 500)
    result = ArchiveExtractor(ARCHIVE_CONFIG).extract(src, tmp_path / 'out', 'gz', depth=0)
    assert result.success is True

def test_path_traversal_rejected(tmp_path):
    src = tmp_path / 'malicious.zip'
    with zipfile.ZipFile(str(src), 'w') as zf:
        info = zipfile.ZipInfo('../../evil.sh')
        zf.writestr(info, b'evil')
        zf.writestr('safe.txt', b'safe content')
    extractor = ArchiveExtractor(ARCHIVE_CONFIG)
    result = extractor.extract(src, tmp_path / 'out', 'zip', depth=0)
    assert any(f.name == 'safe.txt' for f in result.extracted_files)
    assert any('..' in e for e in result.failed_entries)

def test_max_nesting_depth_respected(tmp_path):
    src = tmp_path / 'deep.zip'
    make_zip(src, {'file.txt': b'content'})
    result = ArchiveExtractor(ARCHIVE_CONFIG).extract(src, tmp_path / 'out', 'zip', depth=3)
    assert result.success is False
    assert 'depth' in result.error_message.lower()

def test_stage05_partial_download_quarantined(tmp_path):
    f = tmp_path / 'Unconfirmed 261427.crdownload'
    f.write_bytes(b'partial data')
    out = tmp_path / 'output'
    out.mkdir(exist_ok=True)
    stage = ArchiveIntelligenceStage(ARCHIVE_CONFIG, out)
    _, result = stage.process([f], 'TEST_RUN', out / 'LOGS')
    assert f in result.partial_downloads
    assert f in result.files_quarantined

def test_stage05_cpgz_halted(tmp_path):
    f = tmp_path / 'project.cpgz'
    f.write_bytes(b'\x1f\x8b' + b'\x00' * 50)
    out = tmp_path / 'output'
    out.mkdir(exist_ok=True)
    stage = ArchiveIntelligenceStage(ARCHIVE_CONFIG, out)
    _, result = stage.process([f], 'TEST_RUN', out / 'LOGS')
    assert f in result.recursive_containers

def test_stage05_phase1_format_quarantined(tmp_path):
    f = tmp_path / 'archive.7z'
    f.write_bytes(b'7z\xbc\xaf\x27\x1c' + b'\x00' * 50)
    out = tmp_path / 'output'
    out.mkdir(exist_ok=True)
    stage = ArchiveIntelligenceStage(ARCHIVE_CONFIG, out)
    _, result = stage.process([f], 'TEST_RUN', out / 'LOGS')
    assert f in result.phase1_formats

def test_stage05_zip_extracted_files_added_to_pool(tmp_path):
    archive = tmp_path / 'media.zip'
    make_zip(archive, {'DJI_0001.mp4': b'dji' * 1000, 'IMG_4321.mov': b'iphone' * 500})
    non_archive = tmp_path / 'thumb.png'
    non_archive.write_bytes(b'PNG_DATA')
    out = tmp_path / 'output'
    out.mkdir(exist_ok=True)
    stage = ArchiveIntelligenceStage(ARCHIVE_CONFIG, out)
    expanded, result = stage.process([archive, non_archive], 'TEST_RUN', out / 'LOGS')
    assert non_archive in expanded
    assert len(result.files_extracted) == 2

def test_stage05_archive_manifest_created(tmp_path):
    archive = tmp_path / 'test.zip'
    make_zip(archive, {'file.txt': b'content'})
    out = tmp_path / 'output'
    out.mkdir(exist_ok=True)
    stage = ArchiveIntelligenceStage(ARCHIVE_CONFIG, out)
    _, result = stage.process([archive], 'WEF_TEST', out / 'LOGS')
    assert result.manifest_path is not None
    assert result.manifest_path.exists()

def test_stage05_non_archives_pass_through_unchanged(tmp_path):
    files = [tmp_path / f for f in ['clip.mp4', 'photo.jpg', 'notes.srt']]
    for f in files:
        f.write_bytes(b'media content')
    out = tmp_path / 'output'
    out.mkdir(exist_ok=True)
    stage = ArchiveIntelligenceStage(ARCHIVE_CONFIG, out)
    expanded, result = stage.process(files, 'TEST_RUN', out / 'LOGS')
    assert result.archives_detected == 0
    for f in files:
        assert f in expanded

def test_stage05_disabled_passes_files_unchanged(tmp_path):
    config = dict(ARCHIVE_CONFIG)
    config['archive_engine'] = dict(config['archive_engine'])
    config['archive_engine']['enabled'] = False
    archive = tmp_path / 'test.zip'
    make_zip(archive, {'file.txt': b'content'})
    out = tmp_path / 'output'
    out.mkdir(exist_ok=True)
    stage = ArchiveIntelligenceStage(config, out)
    expanded, result = stage.process([archive], 'TEST_RUN', out / 'LOGS')
    assert result.archives_detected == 0
    assert expanded == [archive]

if __name__ == '__main__':
    import tempfile
    tests = [test_zip_detected_by_magic, test_mislabeled_gz_as_zip_detected,
             test_partial_download_crdownload_detected, test_partial_download_part_detected,
             test_recursive_container_cpgz_detected, test_7z_detected_as_phase1_format,
             test_rar_detected_as_phase1_format, test_non_archive_returns_not_archive,
             test_zip_extraction_produces_files, test_zip_preserves_original,
             test_tar_extraction, test_gz_extraction_single_file,
             test_path_traversal_rejected, test_max_nesting_depth_respected,
             test_stage05_partial_download_quarantined, test_stage05_cpgz_halted,
             test_stage05_phase1_format_quarantined,
             test_stage05_zip_extracted_files_added_to_pool,
             test_stage05_archive_manifest_created,
             test_stage05_non_archives_pass_through_unchanged,
             test_stage05_disabled_passes_files_unchanged]
    passed, failed = [], []
    for fn in tests:
        with tempfile.TemporaryDirectory() as td:
            try:
                fn(Path(td))
                passed.append(fn.__name__)
                print(f'  ✓ {fn.__name__}')
            except Exception as e:
                failed.append(fn.__name__)
                print(f'  ✗ {fn.__name__}: {e}')
    print(f"\n{'='*50}")
    print(f'Stage 0.5: {len(passed)}/{len(passed)+len(failed)} passed', end='')
    print('' if failed else '  — All passed ✓')
