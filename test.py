import PyPDF2


def remove_pdf_password(input_path, output_path, password):
    """
    去除PDF文件的密码保护（需已知正确密码）
    :param input_path: 加密PDF文件路径
    :param output_path: 解密后PDF输出路径
    :param password: PDF文件的解密密码
    """
    try:
        # 以二进制只读模式打开加密PDF
        with open(input_path, 'rb') as input_file:
            # 创建PDF阅读器对象
            pdf_reader = PyPDF2.PdfReader(input_file)

            # 检查PDF是否加密
            if not pdf_reader.is_encrypted:
                print("PDF文件未加密，无需解密")
                return

            # 尝试用密码解密
            if pdf_reader.decrypt(password):
                # 创建PDF写入器对象
                pdf_writer = PyPDF2.PdfWriter()

                # 复制所有页面到写入器
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

                # 写入解密后的PDF文件
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                print(f"密码去除成功，解密文件已保存至: {output_path}")
            else:
                print("密码错误，无法解密PDF")
    except Exception as e:
        print(f"解密过程出错: {str(e)}")


# 使用示例（需替换为实际路径和密码）
if __name__ == "__main__":
    input_pdf = "123.pdf"  # 加密的PDF文件路径
    output_pdf = "123_decrypted.pdf"  # 解密后的输出路径
    pdf_password = "your_password"  # PDF的正确密码

    remove_pdf_password(input_pdf, output_pdf, pdf_password)