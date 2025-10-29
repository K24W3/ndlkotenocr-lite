import os
import xml.etree.ElementTree as ET

def convert_xml_to_svg(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        page = root.find("PAGE")

        if page is None:
            print(f"PAGEタグが見つかりません: {xml_path}")
            return

        width = int(page.attrib.get("WIDTH", 1000))
        height = int(page.attrib.get("HEIGHT", 1000))
        image_name = page.attrib.get("IMAGENAME", "no_image.png")

        svg = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<image href="{image_name}" x="0" y="0" width="{width}" height="{height}" />',
#            f'<!-- Background image: {image_name} (not embedded) -->',
        ]

        # LINEタグ → 赤枠
        for line in page.findall("LINE"):
            x, y = int(line.attrib["X"]), int(line.attrib["Y"])
            w, h = int(line.attrib["WIDTH"]), int(line.attrib["HEIGHT"])
            typ = line.attrib.get("TYPE", "")
            svg.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                f'style="fill:none;stroke:red;stroke-width:5">'
                f'<title>LINE: {typ}</title></rect>'
            )

        # BLOCKタグ → 青枠
        for block in page.findall("BLOCK"):
            x, y = int(block.attrib["X"]), int(block.attrib["Y"])
            w, h = int(block.attrib["WIDTH"]), int(block.attrib["HEIGHT"])
            typ = block.attrib.get("TYPE", "")
            if 3*w < width and typ=="図版":
                svg.append(
                    f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                    f'style="fill:none;stroke:blue;stroke-width:5">'
                    f'<title>BLOCK: {typ}</title></rect>'
                )

        svg.append('</svg>')

        # 出力ファイル名
        svg_path = os.path.splitext(xml_path)[0] + "F.svg"
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write("\n".join(svg))

        print(f"✔ 生成完了: {svg_path}")
    
    except Exception as e:
        print(f"✖ エラー（{xml_path}）: {e}")

def batch_convert(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".xml"):
            xml_path = os.path.join(folder_path, filename)
            convert_xml_to_svg(xml_path)

# === 使用例 ===
# 変換対象フォルダを指定（適宜変更）
target_folder = "../sample_img"  # 例: "./xml_files"
batch_convert(target_folder)

