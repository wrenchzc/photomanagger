from src.imageutils import get_file_info, get_image_info

def test_jpg_tags():
    image_info = get_image_info('data/test1.jpg')
    assert(image_info["image_width"] == 1200)
    assert(image_info["image_height"] == 1600)
    assert(image_info["camera_brand"] == "Canon")
    assert(image_info["focal_length"] == "173/32")

    image_info = get_image_info('data/test2.jpg')
    assert(image_info["image_width"] == 3872)
    assert(image_info["image_height"] == 2592)
    assert(image_info["camera_brand"] == "PENTAX Corporation")
    assert(image_info["focal_length"] == "300")

    image_info = get_image_info('data/noexif.jpg')
    assert(image_info["image_width"] == 608)
    assert(image_info["image_height"] == 874)

def test_file_info():
    file_info = get_file_info('data/test1.jpg')
    assert file_info["md5"] == "060e16eb6c7254076752a480607b3d2c"
    assert file_info["size"] == 762652
    assert file_info["modify_time"] == 1061130716.0
