import argparse
import asyncio

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

parser = argparse.ArgumentParser(description='Baixa vídeos do ArtGrid')
parser.add_argument('link', help='Link da página do vídeo')
parser.add_argument('filename', help='Nome do arquivo para baixar')

args = parser.parse_args()

uid = args.link.split('/')[-2]


async def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    css_selector = f'#main-clipvideo_{uid}_html5_api > source'

    driver.get(args.link)
    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
    finally:
        video_src = driver.find_element(By.CSS_SELECTOR, css_selector).get_attribute(
            'src')

        ffmpeg = (
            FFmpeg()
            .option('y')
            .input(video_src)
            .output(
                f'{args.filename}.mp4',
                vf='scale=-1:1080',
                crf=0
            )
        )

        @ffmpeg.on('progress')
        def on_progress(progress: Progress):
            print(progress)

        @ffmpeg.on('completed')
        def on_completed():
            print(f'Vídeo Convertido e salvo')

        await ffmpeg.execute()
        driver.quit()


if __name__ == '__main__':
    asyncio.run(main())
