from src.imageutils import TagInfo, FileInfo


def test_jpg_tags():
    image_info = TagInfo('data/test1.jpg')
    assert (image_info.image_width == 1200)
    assert (image_info.image_height == 1600)
    assert (image_info.camera_brand == "Canon")
    assert (image_info.focal_length == "173/32")

    image_info = TagInfo('data/test2.jpg')
    assert (image_info.image_width == 3872)
    assert (image_info.image_height == 2592)
    assert (image_info.camera_brand == "PENTAX Corporation")
    assert (image_info.focal_length == "300")

    image_info = TagInfo('data/noexif.jpg')
    assert (image_info.image_width == 608)
    assert (image_info.image_height == 874)


def test_file_info():
    file_info = FileInfo('data/test1.jpg')
    assert file_info.md5 == "060e16eb6c7254076752a480607b3d2c"
    assert file_info.size == 762652

