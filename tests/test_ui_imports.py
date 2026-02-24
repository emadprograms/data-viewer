def test_ui_modules_importable():
    import src.ui.health
    import src.ui.inventory
    import src.ui.inspector

    assert src.ui.health
    assert src.ui.inventory
    assert src.ui.inspector
