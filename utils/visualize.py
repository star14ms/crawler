from nltk import Text
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def show_image(image, axis='off', cmap=None, size=5):
    """
    Parameters
    ----------
        image : array-like or PIL image
    """
    plt.figure(figsize = (size,size))
    plt.imshow(image, cmap=cmap)
    plt.axis(axis)
    plt.show()


def show_images(*images, axis='off', cmap=None, size=25):
    """
    Parameters
    ----------
        *images : array-like or PIL images
    """
    fig, axes = plt.subplots(1, len(images), figsize = (size, size))
    for image, ax in zip(images, axes):
      ax.imshow(image, cmap=cmap)
      ax.axis(axis)
    plt.show()


def plot_frequency_chart(words: Text, top_n=30, size=16, save_path='result/YT_comments_graph.jpg'):
    """데이터의 단어 빈도 수 그래프 그리기"""

    samples = [item for item, _ in words.vocab().most_common(top_n)]
    freqs = [words.vocab()[sample] for sample in samples]
    plt.figure(figsize = (size, size))
    bar = plt.bar(samples, freqs)

    for rect in bar:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % height, ha='center', va='bottom', size=16)

    plt.xlabel('단어')
    plt.ylabel('출현 수 (개)')
    plt.xticks(rotation=60)
    plt.savefig(save_path)
    plt.show()


def draw_word_cloud(words: Text, font_path, width=1000, height=600, background_color="white", size=20, save_path='result/YT_comments_wordcloud.jpg'):
    """학습 데이터의 단어들로 word_cloud 그리기"""

    wc = WordCloud(width=width, height=height, background_color=background_color, font_path=font_path)
    plt.figure(figsize = (size, size))
    plt.imshow(wc.generate_from_frequencies(words.vocab()))
    plt.axis("off")
    plt.savefig(save_path)
    plt.show()
