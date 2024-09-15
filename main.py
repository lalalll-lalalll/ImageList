from PIL import Image
import os
import re

# 生成按数字排序的关键字
def numeric_sort_key(filename):
    numbers = re.findall(r'\d+', filename)
    return [int(num) for num in numbers]

# 调整图像大小并填充以适应目标尺寸
def resize_and_pad_image(img, target_size):
    target_width, target_height = target_size
    original_width, original_height = img.size
    
    # 计算缩放比例
    scale = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    
    # 调整图像大小
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # 创建新的白色背景图像
    new_img = Image.new('RGB', (target_width, target_height), color='white')
    left = (target_width - new_width) // 2
    top = (target_height - new_height) // 2
    new_img.paste(img, (left, top))
    
    return new_img

# 根据给定的顺序将图像排列到A4纸上
def create_a4_image_from_images(image_files, rows, cols, output_file, order='left_to_right'):
    imgs = []
    
    # 打开图像文件并添加到列表中
    for img_file in image_files:
        if img_file:  # 检查文件路径是否有效
            try:
                img = Image.open(img_file)
                imgs.append(img)
            except Exception as e:
                print(f"无法打开文件 {img_file}: {e}")
        else:
            # 创建一个占位图像
            placeholder = Image.new('RGB', (1, 1), color='white')
            imgs.append(placeholder)
    
    # 获取每个图像的最大宽度和高度
    max_width = max(img.width for img in imgs)
    max_height = max(img.height for img in imgs)
    
    # A4纸的尺寸（像素单位）
    a4_width = 2480
    a4_height = 3508
    
    # 计算每个网格单元的尺寸
    grid_width = a4_width // cols
    grid_height = a4_height // rows
    
    # 创建白色背景的A4纸图像
    new_img = Image.new('RGB', (a4_width, a4_height), color='white')
    
    # 根据排列顺序将图像粘贴到A4纸上
    if order == 'left_to_right':
        for idx, img in enumerate(imgs):
            row = idx // cols
            col = idx % cols
            x = col * grid_width
            y = row * grid_height
            img_resized = resize_and_pad_image(img, (grid_width, grid_height))
            new_img.paste(img_resized, (x, y))
    elif order == 'top_to_bottom':
        for idx, img in enumerate(imgs):
            row = idx % rows
            col = idx // rows
            x = col * grid_width
            y = row * grid_height
            img_resized = resize_and_pad_image(img, (grid_width, grid_height))
            new_img.paste(img_resized, (x, y))
    
    # 保存最终生成的图像
    new_img.save(output_file)
    print(f"图片已保存到 {output_file}")

# 获取指定目录中的所有图像文件
def get_image_files(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    return sorted(files, key=lambda f: numeric_sort_key(os.path.basename(f)))

# 主函数
def main():
    image_directory = 'path/to/your/images'  # 图像文件夹路径
    rows = 3  # 行数
    cols = 4  # 列数
    order = 'top_to_bottom'  # 图像排列顺序：'left_to_right' 或 'top_to_bottom'
    
    # 获取排序后的图像文件列表
    image_files = get_image_files(image_directory)
    file_count = rows * cols
    
    # 分批处理图像文件
    for i in range(0, len(image_files), file_count):
        subset_files = image_files[i:i + file_count]
        
        # 如果图像数量不足，填充空图像
        if len(subset_files) < file_count:
            while len(subset_files) < file_count:
                subset_files.append(None)
        
        # 输出文件路径
        output_file = os.path.join(image_directory, f'out_{i // file_count + 1}.png')
        create_a4_image_from_images(subset_files, rows, cols, output_file, order)

if __name__ == "__main__":
    main()
