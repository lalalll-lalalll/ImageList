# ImageList
Input a specified number of images, automatically arrange and output as large images.  
This code uses AI for assisted creation.  
  
输入指定数量的图像，自动排列并输出为大图像.  
代码使用AI进行辅助编写.  

### require
`python 3.6+`  
`pillow`  

### configuration
`path/to/your/images` 输出输入文件夹路径  
`rows` 希望输出图片有几行  
`cols` 希望输出图片有几列  
`order` 先从左往右排列(left_to_right)还是先从上往下排列(top_to_bottom)  

### use
要求输入文件夹图片名称为`n.xxx` (例:1.png,2.png...)  
输出图片与输入图片在同目录,输出图片命名为out_n.png  
输入图片会自动进行比例缩放,若输入图片数量不足会自动使用空白像素占位  
