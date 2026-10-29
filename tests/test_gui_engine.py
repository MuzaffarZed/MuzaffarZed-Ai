import os
import sys
import tempfile
import pytest

# Workspace path
WORKSPACE_PATH = r"C:\Users\MuzaffarZed\ai_workspace"
if WORKSPACE_PATH not in sys.path:
    sys.path.insert(0, WORKSPACE_PATH)

import music_engine
import gui_app


def test_tools_detected():
    """Verify yt-dlp and ffmpeg are found on the system."""
    ytdlp = music_engine.get_ytdlp_path()
    ffmpeg = music_engine.get_ffmpeg_path()
    assert ytdlp is not None, "yt-dlp topilmadi"
    assert ffmpeg is not None, "ffmpeg topilmadi"
    assert os.path.exists(ytdlp)
    assert os.path.exists(ffmpeg)


def test_sanitize_title_variants():
    """Verify title cleaning for auto car stereo display."""
    t1 = "Jaloliddin Ahmadaliyev - Qora ko'z (Official Music Video 2026) [Premyera] 🔥"
    assert music_engine.sanitize_title(t1) == "Jaloliddin Ahmadaliyev - Qora ko'z"

    t2 = "Gulinur - Sevgi | Rasmiy Klip 2026 // HD"
    assert music_engine.sanitize_title(t2) == "Gulinur - Sevgi"

    t3 = "Hamdam Sobirov - Holimga qara [Full Track] 🎧"
    assert music_engine.sanitize_title(t3) == "Hamdam Sobirov - Holimga qara"

    # Test bad characters forbidden in FAT32
    t4 = 'Ozoda Nursaidova: "Yomg\'irlar" / Konsert'
    clean_t4 = music_engine.sanitize_title(t4)
    for forbidden in [':', '"', '/', '\\', '*', '?', '<', '>', '|']:
        assert forbidden not in clean_t4


def test_parse_track_count_free_input():
    """Verify user can type any custom integer or select from preset."""
    assert music_engine.parse_track_count("1") == 1
    assert music_engine.parse_track_count("7") == 7
    assert music_engine.parse_track_count("37 ta") == 37
    assert music_engine.parse_track_count("120") == 120
    assert music_engine.parse_track_count("999") == 200  # Clamped max
    assert music_engine.parse_track_count("abc", default=15) == 15


def test_expanded_catalog_artists_and_styles():
    """Verify 45+ artists across 6 categories and 16+ music styles/genres."""
    artists = music_engine.get_all_artists()
    assert len(artists) >= 45
    assert len(music_engine.ARTIST_CATEGORIES) == 6
    assert len(music_engine.COLLECTIONS_2026) >= 16
    assert len(music_engine.EXTENDED_CAR_FOLDERS) >= 7


def test_smart_sync_and_scan():
    """Verify smart sync detection of existing tracks."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        f1 = os.path.join(tmp_dir, "01 - Jaloliddin Ahmadaliyev - Qora ko'z.mp3")
        f2 = os.path.join(tmp_dir, "02 - Gulinur - Sevgi.mp3")
        with open(f1, "w", encoding="utf-8") as f:
            f.write("dummy")
        with open(f2, "w", encoding="utf-8") as f:
            f.write("dummy")

        existing_set = music_engine.scan_existing_tracks(tmp_dir)
        assert len(existing_set) == 2

        assert music_engine.is_track_already_present("Jaloliddin Ahmadaliyev - Qora ko'z", existing_set) is True
        assert music_engine.is_track_already_present("Gulinur - Sevgi", existing_set) is True
        assert music_engine.is_track_already_present("Konsta - O'zbekiston", existing_set) is False


def test_unified_library_scanner_and_folder_organizer():
    """Verify scan_all_library_mp3s finds songs across all folders and organize_folder_mp3s re-indexes cleanly."""
    with tempfile.TemporaryDirectory() as base_dir:
        dir1 = os.path.join(base_dir, "01_YANGI_XITLAR_2026")
        dir2 = os.path.join(base_dir, "02_SEVIMLI_SANATKORLAR", "Sherali Jo'rayev")
        os.makedirs(dir1, exist_ok=True)
        os.makedirs(dir2, exist_ok=True)

        p1 = os.path.join(dir1, "Qo'shiq Bir (Official Video).mp3")
        p2 = os.path.join(dir2, "Karvon.mp3")
        with open(p1, "wb") as f:
            f.write(b"ID3" + b"\x00" * 4096)
        with open(p2, "wb") as f:
            f.write(b"ID3" + b"\x00" * 4096)

        found_all = music_engine.scan_all_library_mp3s(base_dir, dir1, scan_all=True)
        assert len(found_all) == 2

        found_single = music_engine.scan_all_library_mp3s(base_dir, dir1, scan_all=False)
        assert len(found_single) == 1

        org_res = music_engine.organize_folder_mp3s(dir1)
        assert org_res["total"] == 1
        assert os.path.exists(os.path.join(dir1, "00_Barcha_Qoshiqlar.m3u"))


def test_car_folders_presence():
    """Verify standard automotive folder definitions."""
    assert len(music_engine.CAR_FOLDERS) == 4
    folder_names = [f["folder"] for f in music_engine.CAR_FOLDERS]
    assert "01_YANGI_XITLAR_2026" in folder_names
    assert "02_SEVIMLI_SANATKORLAR" in folder_names
    assert "03_TUNGI_SOKIN_YOL" in folder_names
    assert "04_TOYONA_VA_LAZGI" in folder_names


def test_audiophile_player_instantiation():
    """Verify AudiophilePlayer initializes properly with AIMP transport and seek capabilities."""
    player = music_engine.AudiophilePlayer()
    assert hasattr(player, "is_initialized")
    assert hasattr(player, "toggle_ab")
    assert hasattr(player, "set_volume")
    assert hasattr(player, "seek")
    assert hasattr(player, "step_seek")
    assert hasattr(player, "next_track")
    assert hasattr(player, "prev_track")
    assert hasattr(player, "toggle_repeat")
    assert hasattr(player, "toggle_shuffle")
    assert hasattr(player, "toggle_mute")
    assert player.volume == 0.85
    player.set_volume(0.5)
    assert player.volume == 0.5
    assert player.toggle_repeat() == "ONE"
    assert player.toggle_repeat() == "OFF"
    assert player.toggle_repeat() == "ALL"
    assert player.toggle_shuffle() is True
    assert player.toggle_shuffle() is False


def test_aimp_waveform_and_eq_engine():
    """Verify AIMP 80-bar waveform computation, 10-band EQ filter builder, and metadata reader."""
    assert len(music_engine.AIMP_EQ_FREQS) == 10
    assert len(music_engine.AIMP_EQ_PRESETS) >= 6
    default_preset = music_engine.AIMP_EQ_PRESETS["Maytafon Yumshoq Bass (Standart)"]
    assert len(default_preset) == 10

    eq_str = music_engine.build_eq_ffmpeg_filter(default_preset, preamp_db=1.0)
    assert "equalizer=f=31" in eq_str
    assert "loudnorm=I=-14" in eq_str
    assert "alimiter=limit=-1.2dB" in eq_str

    with tempfile.TemporaryDirectory() as tmp_dir:
        dummy_mp3 = os.path.join(tmp_dir, "01 - Jaloliddin Ahmadaliyev - Yorim.mp3")
        with open(dummy_mp3, "wb") as f:
            f.write(os.urandom(16384))

        wf = music_engine.compute_audio_waveform(dummy_mp3, num_bars=80)
        assert len(wf) == 80
        assert all(0.1 <= v <= 1.0 for v in wf)

        meta = music_engine.read_mp3_metadata(dummy_mp3)
        assert meta["artist"] == "Jaloliddin Ahmadaliyev"
        assert meta["title"] == "Yorim"
        assert len(meta["waveform"]) == 80


def test_playlist_generation():
    """Verify M3U playlist creation in temporary directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        f1 = os.path.join(tmp_dir, "01 - Qo'shiq1.mp3")
        f2 = os.path.join(tmp_dir, "02 - Qo'shiq2.mp3")
        with open(f1, "w", encoding="utf-8") as f:
            f.write("dummy")
        with open(f2, "w", encoding="utf-8") as f:
            f.write("dummy")

        pl_path = music_engine.generate_playlist(tmp_dir, "test.m3u")
        assert pl_path is not None
        assert os.path.exists(pl_path)

        with open(pl_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "#EXTM3U" in content
        assert "01 - Qo'shiq1.mp3" in content
        assert "02 - Qo'shiq2.mp3" in content


def test_idm32_engine_presence():
    """Verify IDM 32-stream downloader engine functions and constants."""
    assert hasattr(music_engine, "download_file_idm32")
    assert callable(music_engine.download_file_idm32)
    assert getattr(music_engine, "DEFAULT_IDM_STREAMS", None) == 32


def test_gui_v8_ultimate_features():
    """Verify MusicCenterApp v8.0 initializes cleanly with 5 Skins, Editable Counts, Interactive Search, and AIMP Studio."""
    app = gui_app.MusicCenterApp()
    assert hasattr(app, "player")
    assert hasattr(app, "btn_ab_toggle")
    assert hasattr(app, "tab_queue")
    assert hasattr(app, "tab_aimp")
    assert hasattr(app, "waveform_seekbar")
    assert hasattr(app, "eq_sliders")
    assert len(app.eq_sliders) == 10
    assert hasattr(app, "combo_target_folder")
    assert hasattr(app, "combo_idm_streams")
    assert hasattr(app, "lbl_idm_speed")
    assert hasattr(app, "visualizer")
    assert hasattr(app, "btn_mini_dock")
    assert hasattr(app, "tab_simulator")

    # Verify editable track count & folder comboboxes (state == 'normal')
    assert app.combo_artist_count.cget("state") == "normal"
    assert app.combo_style_count.cget("state") == "normal"
    assert app.combo_search_count.cget("state") == "normal"
    assert app.combo_target_folder.cget("state") == "normal"

    # Test 5-Skin Dynamic Theme Switching
    for skin_name in gui_app.THEME_SKINS.keys():
        app.apply_skin(skin_name)
        assert app.current_skin_name == skin_name

    # Test interactive search preview rendering
    sample_tracks = [
        {"id": "111", "title": "Jaloliddin Ahmadaliyev - Qora ko'z", "url": "https://www.youtube.com/watch?v=111", "duration": 215, "channel": "Jaloliddin Official"},
        {"id": "222", "title": "Hamdam Sobirov - Malohat", "url": "https://www.youtube.com/watch?v=222", "duration": 198, "channel": "Hamdam Music"},
    ]
    app._render_search_preview_results("Jaloliddin", sample_tracks)
    assert len(app.search_preview_items) == 2
    app._toggle_all_search_checkboxes()
    assert all(not it["var"].get() for it in app.search_preview_items)
    app._toggle_all_search_checkboxes()
    assert all(it["var"].get() for it in app.search_preview_items)

    # Test 3-mode AIMP visualizer toggle (VU -> EQ -> OSC -> VU)
    assert app.visualizer.mode == "VU"
    app.visualizer.toggle_mode()
    assert app.visualizer.mode == "EQ"
    app.visualizer.toggle_mode()
    assert app.visualizer.mode == "OSC"
    app.visualizer.toggle_mode()
    assert app.visualizer.mode == "VU"

    # Test mini-dock toggle
    assert app.is_mini_dock is False
    app._toggle_mini_dock()
    assert app.is_mini_dock is True
    app._toggle_mini_dock()
    assert app.is_mini_dock is False

    # Verify v9.0 Omni-Studio GUI controls
    assert hasattr(app, "btn_loop_a")
    assert hasattr(app, "btn_loop_b")
    assert hasattr(app, "btn_loop_clear")
    assert hasattr(app, "btn_trim_ab")
    assert hasattr(app, "combo_studio_fx")
    assert hasattr(app, "btn_apply_fx")
    assert hasattr(app, "btn_deck_fav")
    assert hasattr(app, "seg_library_scope")
    assert hasattr(app, "combo_library_sort")
    assert hasattr(app, "btn_choose_cover")
    assert hasattr(app, "combo_bitrate")
    assert hasattr(app, "combo_sleep_timer")

    # Test Sleep Timer activation & deactivation
    app._on_sleep_timer_change("15 daqiqa")
    assert app.sleep_timer_end_ts is not None and app.sleep_timer_end_ts > 0
    app._on_sleep_timer_change("O'chiq")
    assert app.sleep_timer_end_ts is None

    app.destroy()


def test_v9_favorites_history_and_usb_export():
    """Verify v9.0 Favorites toggle, History recording, and 1-Click USB export."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        sample_mp3 = os.path.join(tmp_dir, f"01 - Sherali Jo'rayev - O'zbegim_{os.getpid()}.mp3")
        with open(sample_mp3, "wb") as f:
            f.write(b"ID3" + b"\x00" * 2048)

        if music_engine.is_favorite_track(sample_mp3):
            music_engine.toggle_favorite_track(sample_mp3)

        # Toggle favorite ON
        fav_state = music_engine.toggle_favorite_track(sample_mp3)
        assert fav_state is True
        assert music_engine.is_favorite_track(sample_mp3) is True

        # Record play history
        music_engine.record_play_history(sample_mp3)
        state = music_engine.load_user_library_state()
        assert os.path.normcase(os.path.abspath(sample_mp3)) in [
            os.path.normcase(p) for p in state.get("history", [])
        ]

        # Export to USB / target folder
        usb_dir = os.path.join(tmp_dir, "USB_SEVIMLILAR")
        copied_count = music_engine.copy_tracks_to_folder([sample_mp3], usb_dir)
        assert copied_count == 1
        assert os.path.exists(os.path.join(usb_dir, os.path.basename(sample_mp3)))

        # Toggle favorite OFF (clean up state)
        fav_state2 = music_engine.toggle_favorite_track(sample_mp3)
        assert fav_state2 is False
        assert music_engine.is_favorite_track(sample_mp3) is False


def test_v9_omni_studio_fx_and_trimmer_live_ffmpeg():
    """Verify real FFmpeg execution of A-B Audio Trimmer and Studio FX (Slowed+Reverb, 8D)."""
    import subprocess
    ffmpeg = music_engine.get_ffmpeg_path()
    assert ffmpeg is not None

    with tempfile.TemporaryDirectory() as tmp_dir:
        src_mp3 = os.path.join(tmp_dir, "Test_Tone.mp3")
        # Generate a real 4-second stereo sine wave MP3 using FFmpeg
        cmd = [
            ffmpeg, "-y",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=4",
            "-ac", "2", "-ar", "44100", "-b:a", "192k",
            src_mp3
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        assert os.path.exists(src_mp3)

        # 1. Test A-B Segment Trimmer (1.0s to 3.0s)
        trimmed_path = music_engine.trim_mp3_segment(src_mp3, 1.0, 3.0)
        assert trimmed_path is not None, "Trim xatosi"
        assert os.path.exists(trimmed_path)
        assert os.path.getsize(trimmed_path) > 1000

        # 2. Test Studio FX (Slowed + Reverb & 8D Surround)
        fx_path = music_engine.apply_studio_fx_to_track(
            src_mp3, "🌊 Slowed + Reverb (Tungi Atmosfera)", save_as_copy=True
        )
        assert fx_path is not None, "Studio FX Slowed+Reverb xatosi"
        assert os.path.exists(fx_path)
        assert os.path.getsize(fx_path) > 1000

        fx_8d = music_engine.apply_studio_fx_to_track(
            src_mp3, "🎧 8D Surround Audio (360° Aylanuvchi)", save_as_copy=True
        )
        assert fx_8d is not None, "Studio FX 8D xatosi"
        assert os.path.exists(fx_8d)
        assert os.path.getsize(fx_8d) > 1000



