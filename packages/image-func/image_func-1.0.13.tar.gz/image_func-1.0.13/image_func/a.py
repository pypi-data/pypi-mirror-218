from PIL import Image
from scipy.fftpack import fft2, ifft2
import numpy as np
import cv2
import matplotlib.pyplot as plt

def apply_convolution(image, kernel):
    convolved_image = cv2.filter2D(image, -1, kernel)
    return convolved_image

def apply_correlation(image, kernel):
    correlated_image = cv2.filter2D(image, -1, kernel)
    return correlated_image

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)

def process_image(image_path):
    im = Image.open(image_path).convert('L')
    im_array = np.array(im)
    
    freq = fft2(im_array)
    im1 = ifft2(freq).real
    
    snr = signaltonoise(im1, axis=None)
    
    return im_array, im1, snr

def perform_fourier_transform(image_path):
    # Read input image and convert to grayscale
    img = cv2.imread(image_path, 0)

    # Calculate optimal size for Fourier transform
    optimalImg = cv2.copyMakeBorder(img, 0, cv2.getOptimalDFTSize(img.shape[0]) - img.shape[0], 0, cv2.getOptimalDFTSize(img.shape[1]) - img.shape[1], cv2.BORDER_CONSTANT, value=0)

    # Calculate the discrete Fourier transform
    dft_shift = np.fft.fftshift(cv2.dft(np.float32(optimalImg), flags=cv2.DFT_COMPLEX_OUTPUT))

    # Calculate magnitude spectrum
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1)

    # Reconstruct the image using inverse Fourier transform
    result = cv2.magnitude(cv2.idft(np.fft.ifftshift(dft_shift))[:, :, 0], cv2.idft(np.fft.ifftshift(dft_shift))[:, :, 1])

    return optimalImg, magnitude_spectrum, result

def apply_log_transform(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path)

    # Apply log transform
    log_transformed = 255 * np.log(1 + img.astype(np.float32)) / np.log(1 + np.max(img))

    # Convert the data type
    log_transformed = log_transformed.astype(np.uint8)

    # Save the output image
    cv2.imwrite(output_path, log_transformed)



def apply_gamma_correction(image, gamma_values):
    gamma_corrected_images = []

    for gamma in gamma_values:
        gamma_corrected = np.array(255 * (image / 255) ** gamma, dtype='uint8')
        gamma_corrected_images.append(gamma_corrected)

    return gamma_corrected_images





import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image)
    plt.axis('off')

def plot_hist(channel, title=""):
    plt.hist(np.array(channel).ravel(), bins=256, range=(0, 256), color='r', alpha=0.3)
    plt.xlabel('Pixel Values', size=20)
    plt.ylabel('Frequency', size=20)
    plt.title(title, size=10)

def plot_original(im):
    im_r, im_g, im_b = im.split()
    plt.style.use('ggplot')
    plt.figure(figsize=(15, 5))
    plt.subplot(121)
    plot_image(im)
    plt.subplot(122)
    plot_hist(im_r, "Red Channel")
    plot_hist(im_g, "Green Channel")
    plot_hist(im_b, "Blue Channel")
    plt.yscale('log')
    plt.show()

def contrast(c):
    return 0 if c < 50 else (255 if c > 150 else int((255 * c - 22950) / 48))

def plot_stretched(imc):
    im_rc, im_gc, im_bc = imc.split()
    plt.style.use('ggplot')
    plt.figure(figsize=(15, 5))
    plt.subplot(121)
    plot_image(imc)
    plt.subplot(122)
    plot_hist(im_rc, "Contrast-Adjusted Red Channel")
    plot_hist(im_gc, "Contrast-Adjusted Green Channel")
    plot_hist(im_bc, "Contrast-Adjusted Blue Channel")
    plt.yscale('log')
    plt.show()



def histogram_equalization(image):
    hist = cv2.calcHist([image],[0],None,[256],[0,256])
    eq = cv2.equalizeHist(image)
    cdf = hist.cumsum()
    cdfnmhist = cdf * hist.max() / cdf.max()
    histeq = cv2.calcHist([eq],[0],None,[256],[0,256])
    cdfeq = histeq.cumsum()
    cdfnmhisteq = cdfeq * histeq.max() / cdf.max()
    
    return eq, hist, cdfnmhist, histeq, cdfnmhisteq
