from pathlib import Path
import shutil
import pytest
import datetime

from core.file_manager import JsonFileManager
from core.schemas import BaseEvents


class TestFileManager:
  def test_read_json(self):
    file_path = Path("tests/test_data/events.json")
    events = JsonFileManager(file_path).get_all_data()
    assert isinstance(events, list)
    assert len(events) > 0
    assert isinstance(events[0], BaseEvents)

  def test_read_blank_json(self):
    file_path = Path("tests/test_data/blank.json")
    events = JsonFileManager(file_path).get_all_data()
    assert isinstance(events, list)
    assert len(events) == 0
    with pytest.raises(IndexError):
      events[0]

  def test_read_json_not_exist(self):
    file_path = Path("this_file_does_not_exist.json")
    with pytest.raises(FileNotFoundError):
      JsonFileManager(file_path).get_all_data()

  def test_read_empty_json(self):
    file_path = Path("tests/test_data/empty.json")
    with pytest.raises(ValueError):
      JsonFileManager(file_path).get_all_data()

  def test_read_invalid_json(self):
    file_path = Path("tests/test_data/invalid.json")
    with pytest.raises(ValueError):
      JsonFileManager(file_path).get_all_data()

  def test_write_json(self, tmp_path):
    src = Path("tests/test_data/events.json")
    dst = tmp_path / "events.json"
    shutil.copy(src, dst) # copy test data to temp directory

    fileManager = JsonFileManager(dst)
    events_before = fileManager.get_all_data()
    new_event = BaseEvents(message="Test", schedule="daily", dailytime="12:00")
    fileManager.add_new_data(new_event)
    events_after = fileManager.get_all_data()

    assert len(events_after) == len(events_before) + 1
    assert events_after[-1].message == new_event.message 
    assert events_after[-1].schedule == new_event.schedule
    assert events_after[-1].dailytime == new_event.dailytime

  def test_write_json_not_exist(self):
    with pytest.raises(FileNotFoundError):
      JsonFileManager(Path("this_file_does_not_exist.json")).add_new_data(
        BaseEvents(message="Test", schedule="daily", dailytime="12:00")
      )

  def test_update_json(self, tmp_path):
    id_1, idx = 1, 0
    src = Path("tests/test_data/events.json")
    dst = tmp_path / "events.json"
    shutil.copy(src, dst) # copy test data to temp directory

    fileManager = JsonFileManager(dst)
    events_before = fileManager.get_all_data()
    fileManager.update_data(
      key=id_1,
      value=BaseEvents(message="Updated", schedule="once", once="2026-02-15T12:00:00")
    )
    events_after = fileManager.get_all_data()
    updated_event = fileManager.get_data_by_id(id_1)

    assert len(events_after) == len(events_before)
    assert updated_event.id == id_1
    assert events_before[idx].message == "Test event"
    assert events_before[idx].schedule.value == "daily"
    assert events_before[idx].dailytime == datetime.time(12, 0) 
    assert updated_event.message == "Updated"
    assert updated_event.schedule.value == "once"
    assert updated_event.once == datetime.datetime(2026, 2, 15, 12, 0)

  def test_delete_json(self, tmp_path):
    id_1 = 1
    src = Path("tests/test_data/events.json")
    dst = tmp_path / "events.json"
    shutil.copy(src, dst) # copy test data to temp directory

    fileManager = JsonFileManager(dst)
    events_before = fileManager.get_all_data()
    fileManager.delete_data(id_1)
    events_after = fileManager.get_all_data()

    assert len(events_after) == len(events_before) - 1
    assert events_after == []