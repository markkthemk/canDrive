from gui.can_sniffer_main_window import CanSnifferMainWindow


def test_new_project(qtbot, monkeypatch, tmp_path):
    def mock_return_sniff_save(*args):
        project_sniff = tmp_path / "project_1.sniff"
        with open(project_sniff, "w") as f:
            f.write("")
        return project_sniff

    monkeypatch.setattr("core.user_preferences.SAVE_LOCATION", tmp_path / "user_preferences.yaml")
    monkeypatch.setattr("gui.can_sniffer_main_window.CanSnifferMainWindow.show_new_file_dialog",
                        mock_return_sniff_save)

    main_window = CanSnifferMainWindow()

    assert main_window.windowTitle() == "Can Sniffer"

    assert main_window.act_new.isEnabled()
    assert main_window.act_open.isEnabled()
    assert main_window.act_open_legacy.isEnabled()
    assert not main_window.act_close.isEnabled()

    assert not main_window.act_1_live_mode_tab.isEnabled()
    assert not main_window.act_2_playback_mode_tab.isEnabled()
    assert not main_window.act_3_decoded_messages_tab.isEnabled()
    assert not main_window.act_4_label_dictionary_tab.isEnabled()

    main_window.on_new_project()

    assert main_window.windowTitle() == f"Can Sniffer - {tmp_path / 'project_1.sniff'}"

    assert not main_window.act_new.isEnabled()
    assert not main_window.act_open.isEnabled()
    assert not main_window.act_open_legacy.isEnabled()
    assert main_window.act_close.isEnabled()

    assert main_window.act_1_live_mode_tab.isEnabled()
    assert main_window.act_2_playback_mode_tab.isEnabled()
    assert main_window.act_3_decoded_messages_tab.isEnabled()
    assert main_window.act_4_label_dictionary_tab.isEnabled()

    main_window.on_project_close()

    assert main_window.act_new.isEnabled()
    assert main_window.act_open.isEnabled()
    assert main_window.act_open_legacy.isEnabled()
    assert not main_window.act_close.isEnabled()

    assert not main_window.act_1_live_mode_tab.isEnabled()
    assert not main_window.act_2_playback_mode_tab.isEnabled()
    assert not main_window.act_3_decoded_messages_tab.isEnabled()
    assert not main_window.act_4_label_dictionary_tab.isEnabled()

    main_window.close()

    main_window = CanSnifferMainWindow()
    assert main_window.windowTitle() == f"Can Sniffer - {tmp_path / 'project_1.sniff'}"
    main_window.on_project_close()
    assert main_window.windowTitle() == "Can Sniffer"
