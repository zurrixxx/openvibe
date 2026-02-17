def test_package_importable():
    import openvibe_sdk
    assert openvibe_sdk.__doc__ is not None
