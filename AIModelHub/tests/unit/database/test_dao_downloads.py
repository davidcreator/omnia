"""
Testes unitários — database/dao_downloads.py
"""

import pytest
from database.dao_downloads import DAODownloads


@pytest.mark.unit
class TestDAODownloadsCreate:
    """Testa criação de downloads."""

    def test_create_basic(self, dao_downloads):
        download_id = dao_downloads.create(
            url="https://huggingface.co/model.gguf",
        )
        assert download_id is not None
        assert download_id > 0

    def test_create_with_all_fields(self, dao_downloads):
        download_id = dao_downloads.create(
            url="https://huggingface.co/model.gguf",
            model_name="Llama 3 8B",
            size_bytes=4_500_000_000,
        )
        result = dao_downloads.get_by_id(download_id)
        assert result["model_name"] == "Llama 3 8B"
        assert result["size_bytes"] == 4_500_000_000

    def test_create_default_status_pending(self, dao_downloads):
        download_id = dao_downloads.create(url="https://example.com/model.gguf")
        result = dao_downloads.get_by_id(download_id)
        assert result["status"] == DAODownloads.STATUS_PENDING

    def test_create_default_progress_zero(self, dao_downloads):
        download_id = dao_downloads.create(url="https://example.com/model.gguf")
        result = dao_downloads.get_by_id(download_id)
        assert result["progress"] == 0


@pytest.mark.unit
class TestDAODownloadsRead:
    """Testa leitura de downloads."""

    def test_get_by_id_existing(self, dao_downloads):
        did = dao_downloads.create(url="https://example.com/model.gguf")
        result = dao_downloads.get_by_id(did)
        assert result is not None

    def test_get_by_id_nonexistent(self, dao_downloads):
        result = dao_downloads.get_by_id(99999)
        assert result is None

    def test_get_pending(self, dao_downloads):
        dao_downloads.create(url="https://example.com/model1.gguf")
        dao_downloads.create(url="https://example.com/model2.gguf")
        result = dao_downloads.get_pending()
        assert len(result) == 2

    def test_get_active_empty(self, dao_downloads):
        dao_downloads.create(url="https://example.com/model.gguf")
        result = dao_downloads.get_active()
        assert result == []

    def test_get_all(self, dao_downloads):
        dao_downloads.create(url="https://example.com/model1.gguf")
        dao_downloads.create(url="https://example.com/model2.gguf")
        result = dao_downloads.get_all()
        assert len(result) == 2


@pytest.mark.unit
class TestDAODownloadsUpdateStatus:
    """Testa atualização de status."""

    def test_mark_active(self, dao_downloads):
        did = dao_downloads.create(url="https://example.com/model.gguf")
        dao_downloads.mark_active(did)
        result = dao_downloads.get_by_id(did)
        assert result["status"] == DAODownloads.STATUS_ACTIVE

    def test_mark_completed(self, dao_downloads):
        did = dao_downloads.create(url="https://example.com/model.gguf")
        dao_downloads.mark_completed(did)
        result = dao_downloads.get_by_id(did)
        assert result["status"] == DAODownloads.STATUS_COMPLETED

    def test_mark_failed(self, dao_downloads):
        did = dao_downloads.create(url="https://example.com/model.gguf")
        dao_downloads.mark_failed(did)
        result = dao_downloads.get_by_id(did)
        assert result["status"] == DAODownloads.STATUS_FAILED

    def test_mark_cancelled(self, dao_downloads):
        did = dao_downloads.create(url="https://example.com/model.gguf")
        dao_downloads.mark_cancelled(did)
        result = dao_downloads.get_by_id(did)
        assert result["status"] == DAODownloads.STATUS_CANCELLED


@pytest.mark.unit
class TestDAODownloadsUpdateProgress:
    """Testa atualização de progresso."""

    def test_update_progress(self, dao_downloads):
        did = dao_downloads.create(url="https://example.com/model.gguf")
        dao_downloads.update_progress(did, 50.0)
        result = dao_downloads.get_by_id(did)
        assert result["progress"] == pytest.approx(50.0)

    def test_update_progress_clamp_max(self, dao_downloads):
        did = dao_downloads.create(url="https://example.com/model.gguf")
        dao_downloads.update_progress(did, 150.0)
        result = dao_downloads.get_by_id(did)
        assert result["progress"] == pytest.approx(100.0)

    def test_update_progress_clamp_min(self, dao_downloads):
        did = dao_downloads.create(url="https://example.com/model.gguf")
        dao_downloads.update_progress(did, -10.0)
        result = dao_downloads.get_by_id(did)
        assert result["progress"] == pytest.approx(0.0)


@pytest.mark.unit
class TestDAODownloadsDelete:
    """Testa remoção de downloads."""

    def test_delete_existing(self, dao_downloads):
        did = dao_downloads.create(url="https://example.com/model.gguf")
        result = dao_downloads.delete(did)
        assert result is True
        assert dao_downloads.get_by_id(did) is None

    def test_delete_nonexistent(self, dao_downloads):
        result = dao_downloads.delete(99999)
        assert result is False

    def test_clear_completed(self, dao_downloads):
        d1 = dao_downloads.create(url="https://example.com/1.gguf")
        d2 = dao_downloads.create(url="https://example.com/2.gguf")
        dao_downloads.mark_completed(d1)
        dao_downloads.mark_completed(d2)
        count = dao_downloads.clear_completed()
        assert count == 2

    def test_clear_failed(self, dao_downloads):
        d1 = dao_downloads.create(url="https://example.com/1.gguf")
        dao_downloads.mark_failed(d1)
        count = dao_downloads.clear_failed()
        assert count == 1


@pytest.mark.unit
class TestDAODownloadsAgregations:
    """Testa agregações."""

    def test_count_empty(self, dao_downloads):
        assert dao_downloads.count() == 0

    def test_count_total(self, dao_downloads):
        dao_downloads.create(url="https://example.com/1.gguf")
        dao_downloads.create(url="https://example.com/2.gguf")
        assert dao_downloads.count() == 2

    def test_count_by_status(self, dao_downloads):
        d1 = dao_downloads.create(url="https://example.com/1.gguf")
        dao_downloads.mark_completed(d1)
        dao_downloads.create(url="https://example.com/2.gguf")
        assert dao_downloads.count(DAODownloads.STATUS_COMPLETED) == 1
        assert dao_downloads.count(DAODownloads.STATUS_PENDING) == 1

    def test_get_total_downloaded_bytes(self, dao_downloads):
        d1 = dao_downloads.create(
            url="https://example.com/1.gguf",
            size_bytes=1_000_000,
        )
        d2 = dao_downloads.create(
            url="https://example.com/2.gguf",
            size_bytes=2_000_000,
        )
        dao_downloads.mark_completed(d1)
        dao_downloads.mark_completed(d2)
        total = dao_downloads.get_total_downloaded_bytes()
        assert total == 3_000_000