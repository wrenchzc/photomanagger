from photomanager.utils.imageutils import TagInfo, FileInfo


def test_jpg_tags():
    image_info = TagInfo('tests/data/test1.jpg')
    assert (image_info.image_width == 1200)
    assert (image_info.image_height == 1600)
    assert (image_info.camera_brand == "Canon")
    assert (image_info.focal_length == "173/32")

    image_info = TagInfo('tests/data/test2.jpg')
    assert (image_info.image_width == 3648)
    assert (image_info.image_height == 2736)
    assert (image_info.camera_brand == "HUAWEI")
    assert (image_info.camera_type == "LYA-AL00")
    assert (image_info.focal_length == "187/25")
    assert (image_info.latitude == "N|[25, 44, 23236999/1000000]")
    assert (image_info.longitude == "E|[113, 44, 7412567/250000]")
    assert (image_info.orientation == 0)

    image_info = TagInfo('tests/data/noexif.jpg')
    assert (image_info.image_width == 608)
    assert (image_info.image_height == 874)


def test_file_info():
    file_info = FileInfo('tests/data/test1.jpg')
    assert file_info.md5 == "060e16eb6c7254076752a480607b3d2c"
    assert file_info.size == 762652

