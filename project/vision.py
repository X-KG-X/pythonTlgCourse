{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Computer Vision\n",
    "This notebook includes some examples of techniques used to analyze images - which is a common requirement in AI solutions.\n",
    "\n",
    "## Manipulating Images\n",
    "As far as computers are concerned, images are simply numerical data representations. You can use statistical techniques to manipulate and analyze the numerical properties of images.\n",
    "\n",
    "### Load an Image\n",
    "Let's start by loading a JPG file and examining its properties. Run the following cell to load and display an image."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline\n",
    "from matplotlib.pyplot import imshow\n",
    "from PIL import Image\n",
    "import numpy as np\n",
    "import skimage.color as sc\n",
    "\n",
    "!curl https://raw.githubusercontent.com/MicrosoftLearning/AI-Introduction/master/files/graeme2.jpg -o img.jpg\n",
    "\n",
    "i = np.array(Image.open('img.jpg'))\n",
    "imshow(i)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Examine Numerical Properties of the Image\n",
    "You can clearly see that this is an image, but how does the computer interpret the data?\n",
    "\n",
    "Run the cell below to determine the data type of the image."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "type(i)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The image data is actually stored as a multi-dimensional array.\n",
    "\n",
    "Let's see what data type the array elements are:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "i.dtype"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "OK, so the array consists of 8-bit integer values. In other words, whole numbers between 0 and 255.\n",
    "\n",
    "Now let's examine the shape of the array:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "i.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "So the image data is a three dimensional 433 x 650 x 3 array.\n",
    "\n",
    "This is a RGB color JPG image sized 433 x 650 pixels. The image includes pixel values for red, green, and blue color channels. \n",
    "\n",
    "To keep things simple, let's convert the image to a greyscale image so we only have one color channel dimension to deal with:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "i_mono = sc.rgb2gray(i)\n",
    "imshow(i_mono, cmap='gray')\n",
    "i_mono.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### View Pixel Value Distributions\n",
    "Let's look at the distribution of pixel values in the image. Ideally, the image should have relatively even distribution of values, indicating good contrast and making it easier to extract analytical information.\n",
    "\n",
    "An easy way to check this is to plot a histogram."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def im_hist(img):\n",
    "    import matplotlib.pyplot as plt    \n",
    "    fig = plt.figure(figsize=(8, 6))\n",
    "    fig.clf()\n",
    "    ax = fig.gca()    \n",
    "    ax.hist(img.flatten(), bins = 256)\n",
    "    plt.show()\n",
    "\n",
    "im_hist(i_mono)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Another useful way to visualize the statistics of an image is as a cumulative distribution function (CDF) plot. Ideally, this should result in a fairly straight diagonal line."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def im_cdf(img):\n",
    "    import matplotlib.pyplot as plt    \n",
    "    fig = plt.figure(figsize=(8, 6))\n",
    "    fig.clf()\n",
    "    ax = fig.gca()    \n",
    "    ax.hist(img.flatten(), bins = 256, cumulative=True)\n",
    "    plt.show()\n",
    "    \n",
    "im_cdf(i_mono)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The histogram and CDF for our image show pretty uneven distribution. Ideally we should equalize the values in the image to improve its analytical value.\n",
    "\n",
    "### Equalize the Image\n",
    "Histogram equalization is often used to improve the statistics of images. In simple terms, the histogram equalization algorithm attempts to adjust the pixel values in the image to create a more uniform distribution. The code in the cell below uses the  **exposure.equalize_hist** method from the **skimage** package to equalize the image.  "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from skimage import exposure\n",
    "\n",
    "i_eq = exposure.equalize_hist(i_mono)\n",
    "imshow(i_eq, cmap='gray')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now let's see what that's done to the histogram and CDF plots:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "im_hist(i_eq)\n",
    "im_cdf(i_eq)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The pixel intensities are more evenly distributed in the equalized image."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Denoising with Filters\n",
    "\n",
    "Often images need to be cleaned up to remove \"salt and pepper\" noise."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Add Some Random Noise\n",
    "Let's add some random noise to our image - such as you might see in a photograph taken in low light or at a low resolution."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import skimage\n",
    "i_n = skimage.util.random_noise(i_eq)\n",
    "imshow(i_n, cmap=\"gray\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Using a Gaussian Filter\n",
    "A Gaussian filter applies a weighted average (mean) value for pixels based on the pixels that surround them."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def gauss_filter(im, sigma = 2):\n",
    "    from scipy.ndimage.filters import gaussian_filter as gf\n",
    "    import numpy as np\n",
    "    return gf(im, sigma = sigma)   \n",
    "i_g = gauss_filter(i_n)\n",
    "imshow(i_g, cmap=\"gray\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Using a Median Filter\n",
    "The Gaussian filter results in a blurred image - we could try a median filter, which as the name suggests applies the median value to pixels based on the pixels around them."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def med_filter(im, size = 2):\n",
    "    from scipy.ndimage.filters import median_filter as mf\n",
    "    import numpy as np\n",
    "    return mf(im, size = size)     \n",
    "i_m = med_filter(i_n)\n",
    "imshow(i_m, cmap=\"gray\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Extract Features\n",
    "Now that we've done some initial processing of the image to improve its statistics for analysis, we can start to extract features from it.\n",
    "#### Sobel Edge Detection\n",
    "As a first step in extracting features, you will apply the Sobel edge detection algorithm. This finds regions of the image with large gradient values in multiple directions. Regions with high omnidirectional gradient are likely to be edges or transitions in the pixel values. \n",
    "\n",
    "The code in the cell below applies the Sobel algorithm to the median filtered image, using these steps:\n",
    "\n",
    "    1. Convert the color, rgb, image to grayscale (in this case, the image is already grayscale - but you should always do this because using a grayscale image simplifies the gradient calculation since it is two dimensional.\n",
    "    2. Computer the gradient in the x and y (horizontal and vertical) directions. \n",
    "    3. Compute the magnitude of the gradient.\n",
    "    4. Normalize the gradient values. \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def edge_sobel(image):\n",
    "    from scipy import ndimage\n",
    "    import skimage.color as sc\n",
    "    import numpy as np\n",
    "    image = sc.rgb2gray(image) # Convert color image to gray scale\n",
    "    dx = ndimage.sobel(image, 1)  # horizontal derivative\n",
    "    dy = ndimage.sobel(image, 0)  # vertical derivative\n",
    "    mag = np.hypot(dx, dy)  # magnitude\n",
    "    mag *= 255.0 / np.amax(mag)  # normalize (Q&D)\n",
    "    mag = mag.astype(np.uint8)\n",
    "    return mag\n",
    "\n",
    "i_edge = edge_sobel(i_m)\n",
    "imshow(i_edge, cmap=\"gray\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now let's try with the more blurred gaussian filtered image."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "i_edge = edge_sobel(i_g)\n",
    "imshow(i_edge, cmap=\"gray\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Note that the lines are more pronounced. Although a gaussian filter makes the image blurred to human eyes, this blurring can actually help accentuate contrasting features."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Harris Corner Detection\n",
    "Another example of a feature extraction algorithm is corner detection. In simple terms, the Harris corner detection algorithm locates regions of the image with large changes in pixel values in all directions. These regions are said to be corners. The Harris corner detector is paired with the **corner_peaks** method. This operator filters the output of the Harris algorithm, over a patch of the image defined by the span of the filters, for the most likely corners."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Function to apply the Harris corner-detection algorithm to an image\n",
    "def corner_harr(im, min_distance = 20):\n",
    "    from skimage.feature import corner_harris, corner_peaks\n",
    "    mag = corner_harris(im)\n",
    "    return corner_peaks(mag, min_distance = min_distance)\n",
    "\n",
    "# Find the corners in the median filtered image with a minimum distance of 20 pixels\n",
    "harris = corner_harr(i_m, 20)\n",
    "\n",
    "print (harris)\n",
    "\n",
    "# Function to plot the image with the harris corners marked on it\n",
    "def plot_harris(im, harris, markersize = 20, color = 'red'):\n",
    "    import matplotlib.pyplot as plt\n",
    "    import numpy as np\n",
    "    fig = plt.figure(figsize=(6, 6))\n",
    "    fig.clf()\n",
    "    ax = fig.gca()    \n",
    "    ax.imshow(np.array(im).astype(float), cmap=\"gray\")\n",
    "    ax.plot(harris[:, 1], harris[:, 0], 'r+', color = color, markersize=markersize)\n",
    "    return 'Done'  \n",
    "\n",
    "plot_harris(i_m, harris)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The corner detection algorithm has identified the eyes in the image."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "collapsed": true
   },
   "source": [
    "## Using the Computer Vision API\n",
    "The techniques used so far in this notebook show how you can perform simple image amnipulation and apply some popular algorithms to analyze images. More complex image analysis capabilities are encapsulated in the Computer Vision API cognitive service.\n",
    "\n",
    "### Create a Computer Vision API Service\n",
    "To provision a Computer Vision API service in your Azure subscription, Follow these steps:\n",
    "\n",
    "1. Open another browser tab and navigate to https://portal.azure.com.\n",
    "2. Sign in using your Microsoft account.\n",
    "3. Click **+ New**, and in the **AI + Cognitive Services** category, click **See all**.\n",
    "4. In the list of cognitive services, click **Computer Vision API**.\n",
    "5. In the **Computer Vision API** blade, click **Create**.\n",
    "6. In the **Create** blade, enter the following details, and then click **Create**\n",
    "  * **Name**: A unique name for your service.\n",
    "  * **Subscription**: Your Azure subscription.\n",
    "  * **Location**: Choose the Azure datacenter location where you want to host your service.\n",
    "  * **Pricing tier**: Choose the F0 pricing tier.\n",
    "  * **Resource Group**: Choose the existing resource group you created in the previous lab (or create a new one if you didn't complete the previous lab)\n",
    "  * Read the notice about the use of your data, and select the checkbox.\n",
    "7. Wait for the service to be created.\n",
    "8. When deployment is complete, click **All Resources** and then click your Computer Vision service to open its blade.\n",
    "9. In the blade for your Computer Vision service, note the **Endpoint** URL. Then assign the base URI (*location*.api.cognitive.microsoft.com) for your service to the **visionURI** variable in the cell below.\n",
    "10. In the blade for your Computer Vision service, click **Keys** and then copy **Key 1** to the clipboard and paste it into the **visionKey** variable assignment value in the cell below. \n",
    "11. Run the cell below to assign the variables.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "visionURI = 'LOCATION.api.cognitive.microsoft.com'\n",
    "visionKey = 'YOUR_KEY'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Get An Image from a URL\n",
    "Let's start with the same image we analyzed previously.\n",
    "\n",
    "Run the code in the cell below to retrieve the original color image from its URL:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline\n",
    "from matplotlib.pyplot import imshow\n",
    "from PIL import Image\n",
    "import requests\n",
    "from io import BytesIO\n",
    "\n",
    "img_url = 'https://raw.githubusercontent.com/MicrosoftLearning/AI-Introduction/master/files/graeme2.jpg'\n",
    "\n",
    "# Get the image and show it\n",
    "response = requests.get(img_url)\n",
    "img = Image.open(BytesIO(response.content))\n",
    "imshow(img)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Use the Computer Vision API to Get Image Features\n",
    "The Computer Vision API uses a machine learning model that has been trtained with millions of images. It can extract features from images and return a suggested description, as well as details about the image file and a suggested list of \"tags\" that apply to it.\n",
    "\n",
    "Run the cell below to see what caption the Computer Vision API suggests for the image above."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_image_features(img_url):\n",
    "    import http.client, urllib.request, urllib.parse, urllib.error, base64, json\n",
    "\n",
    "    headers = {\n",
    "        # Request headers.\n",
    "        'Content-Type': 'application/json',\n",
    "        'Ocp-Apim-Subscription-Key': visionKey,\n",
    "    }\n",
    "\n",
    "    params = urllib.parse.urlencode({\n",
    "        # Request parameters. All of them are optional.\n",
    "        'visualFeatures': 'Categories,Description,Color',\n",
    "        'language': 'en',\n",
    "    })\n",
    "\n",
    "    body = \"{'url':'\" + img_url + \"'}\"\n",
    "\n",
    "    try:\n",
    "        # Execute the REST API call and get the response.\n",
    "        conn = http.client.HTTPSConnection(visionURI)\n",
    "        conn.request(\"POST\", \"/vision/v1.0/analyze?%s\" % params, body, headers)\n",
    "        response = conn.getresponse()\n",
    "        data = response.read()\n",
    "\n",
    "        # 'data' contains the JSON response.\n",
    "        parsed = json.loads(data.decode(\"UTF-8\"))\n",
    "        if response is not None:\n",
    "            return parsed\n",
    "        conn.close()\n",
    "\n",
    "\n",
    "    except Exception as e:\n",
    "        print('Error:')\n",
    "        print(e)\n",
    "        \n",
    "jsonData = get_image_features(img_url)\n",
    "desc = jsonData['description']['captions'][0]['text']\n",
    "print(desc)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The description is reasonably, if not exactly, appropriate.\n",
    "\n",
    "Run the cell below to see the full JSON response, including image properties and suggested tags."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "\n",
    "# View the full details returned\n",
    "print (json.dumps(jsonData, sort_keys=True, indent=2))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's try with a different image:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "img_url = 'https://raw.githubusercontent.com/MicrosoftLearning/AI-Introduction/master/files/uke.jpg'\n",
    "\n",
    "# Get the image and show it\n",
    "response = requests.get(img_url)\n",
    "img = Image.open(BytesIO(response.content))\n",
    "imshow(img)\n",
    "jsonData = get_image_features(img_url)\n",
    "desc = jsonData['description']['captions'][0]['text']\n",
    "print(desc)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "How about something a little more complex?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "img_url = 'https://raw.githubusercontent.com/MicrosoftLearning/AI-Introduction/master/files/soccer.jpg'\n",
    "\n",
    "# Get the image and show it\n",
    "response = requests.get(img_url)\n",
    "img = Image.open(BytesIO(response.content))\n",
    "imshow(img)\n",
    "jsonData = get_image_features(img_url)\n",
    "desc = jsonData['description']['captions'][0]['text']\n",
    "print(desc)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Using the Face API\n",
    "While the Computer Vision API is useful for general image analysis, the Face API offers specific functions for analyzing faces in images. This can be useful in a variety of AI scenarios.\n",
    "\n",
    "### Create a Face API Service\n",
    "To provision a Computer Vision API service in your Azure subscription, Follow these steps:\n",
    "\n",
    "1. Open another browser tab and navigate to https://portal.azure.com.\n",
    "2. Sign in using your Microsoft account.\n",
    "3. Click **+ New**, and in the **AI + Cognitive Services** category, click **See all**.\n",
    "4. In the list of cognitive services, click **Face API**.\n",
    "5. In the **Face API** blade, click **Create**.\n",
    "6. In the **Create** blade, enter the following details, and then click **Create**\n",
    "  * **Name**: A unique name for your service.\n",
    "  * **Subscription**: Your Azure subscription.\n",
    "  * **Location**: Choose the Azure datacenter location where you want to host your service.\n",
    "  * **Pricing tier**: Choose the F0 pricing tier.\n",
    "  * **Resource Group**: Choose the existing resource group you created in the previous lab (or create a new one if you didn't complete the previous lab)\n",
    "  * Read the notice about the use of your data, and select the checkbox.\n",
    "7. Wait for the service to be created.\n",
    "8. When deployment is complete, click **All Resources** and then click your Face service to open its blade.\n",
    "9. In the blade for your Face service, copy the *full* **Endpoint** URL (including the *https* prefix and */face/v1.0/* path), and paste it into the **faceURI** variable assignment value in the cell below.\n",
    "10. In the blade for your Face service, click **Keys** and then copy **Key 1** to the clipboard and paste it into the **faceKey** variable assignment value in the cell below. \n",
    "11. Run the cell below to assign the variables."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "faceURI = \"https://LOCATION.api.cognitive.microsoft.com/face/v1.0/\"\n",
    "faceKey = \"YOUR_KEY\""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The Face API has a Python SDK, which you can install as a package. This makes it easier to work with.\n",
    "\n",
    "Run the following cell to install the Face API SDK and the pillow package (which is used to work with images)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install cognitive_face\n",
    "!pip install pillow"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now you're ready to use the Face API. First, let's see if we can detect a face in an image:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import cognitive_face as CF\n",
    "\n",
    "# Set URI and Key\n",
    "CF.BaseUrl.set(faceURI)\n",
    "CF.Key.set(faceKey)\n",
    "\n",
    "\n",
    "# Detect faces in an image\n",
    "img_url = 'https://raw.githubusercontent.com/MicrosoftLearning/AI-Introduction/master/files/graeme1.jpg'\n",
    "result = CF.face.detect(img_url)\n",
    "print (result)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The Face API has detected one face, and assigned it an ID. It also returns the coordinates for the top left corner and the width and height for the rectangle within which the face is detected.\n",
    "\n",
    "Run the cell below to show the rectange on the image."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline\n",
    "import requests\n",
    "from io import BytesIO\n",
    "from matplotlib.pyplot import imshow\n",
    "from PIL import Image, ImageDraw\n",
    "\n",
    "# Get the image\n",
    "response = requests.get(img_url)\n",
    "img = Image.open(BytesIO(response.content))\n",
    "\n",
    "# Add rectangles for each face found\n",
    "color=\"blue\"\n",
    "if result is not None:\n",
    "    draw = ImageDraw.Draw(img) \n",
    "    for currFace in result:\n",
    "        faceRectangle = currFace['faceRectangle']\n",
    "        left = faceRectangle['left']\n",
    "        top = faceRectangle['top']\n",
    "        width = faceRectangle['width']\n",
    "        height = faceRectangle['height']\n",
    "        draw.line([(left,top),(left+width,top)],fill=color, width=5)\n",
    "        draw.line([(left+width,top),(left+width,top+height)],fill=color , width=5)\n",
    "        draw.line([(left+width,top+height),(left, top+height)],fill=color , width=5)\n",
    "        draw.line([(left,top+height),(left, top)],fill=color , width=5)\n",
    "\n",
    "# show the image\n",
    "imshow(img)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "As well as detecting the face, the Face API assigned an ID to this face. The ID is retained by the service for a while, enabling you to reference it. Run the following cell to see the ID assigned to the face that has been detected:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "face1 = result[0]['faceId']\n",
    "print (\"Face 1:\" + face1)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "One useful thing you can do with the face ID is, is to use it to compare another image and see if a matching face is found. This kind of facial comparison is common in a variety of security / user authentication scenarios.\n",
    "\n",
    "Let's try it with another image of the same person:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Get the image to compare\n",
    "img2_url = 'https://raw.githubusercontent.com/MicrosoftLearning/AI-Introduction/master/files/graeme2.jpg'\n",
    "response2 = requests.get(img2_url)\n",
    "img2 = Image.open(BytesIO(response2.content))\n",
    "\n",
    "# Detect faces in a comparison image\n",
    "result2 = CF.face.detect(img2_url)\n",
    "\n",
    "# Assume the first face is the one we want to compare\n",
    "if result2 is not None:\n",
    "    face2 = result2[0]['faceId']\n",
    "    print (\"Face 2:\" + face2)\n",
    "\n",
    "def verify_face(face1, face2):\n",
    "    # By default, assume the match is unverified\n",
    "    verified = \"Not Verified\"\n",
    "    color=\"red\"\n",
    "\n",
    "    # compare the comparison face to the original one we retrieved previously\n",
    "    verify = CF.face.verify(face1, face2)\n",
    "\n",
    "    # if there's a match, set verified and change color to green\n",
    "    if verify['isIdentical'] == True:\n",
    "        verified = \"Verified\"\n",
    "        color=\"lightgreen\"\n",
    "\n",
    "    # Display the second face with a red rectange if unverified, or green if verified\n",
    "    draw = ImageDraw.Draw(img2) \n",
    "    for currFace in result2:\n",
    "        faceRectangle = currFace['faceRectangle']\n",
    "        left = faceRectangle['left']\n",
    "        top = faceRectangle['top']\n",
    "        width = faceRectangle['width']\n",
    "        height = faceRectangle['height']\n",
    "        draw.line([(left,top),(left+width,top)] , fill=color, width=5)\n",
    "        draw.line([(left+width,top),(left+width,top+height)] , fill=color, width=5)\n",
    "        draw.line([(left+width,top+height),(left, top+height)] , fill=color, width=5)\n",
    "        draw.line([(left,top+height),(left, top)] , fill=color, width=5)\n",
    "\n",
    "    # show the image\n",
    "    imshow(img2)\n",
    "\n",
    "    # Display verification status and confidence level\n",
    "    print(verified)\n",
    "    print (\"Confidence Level: \" + str(verify['confidence']))\n",
    "\n",
    "verify_face(face1, face2)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The service has matched the face in a similar photo, with a reasonably high confidence level.\n",
    "\n",
    "But what about the same face in a different photo - maybe with a stylish goatee beard and sunglasses?:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Get the image to compare\n",
    "img2_url = 'https://raw.githubusercontent.com/MicrosoftLearning/AI-Introduction/master/files/graeme3.jpg'\n",
    "response2 = requests.get(img2_url)\n",
    "img2 = Image.open(BytesIO(response2.content))\n",
    "\n",
    "# Detect faces in a comparison image\n",
    "result2 = CF.face.detect(img2_url)\n",
    "\n",
    "# Assume the first face is the one we want to compare\n",
    "face2 = result2[0]['faceId']\n",
    "print (\"Face 2:\" + face2)\n",
    "\n",
    "verify_face(face1, face2)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Again, the face is matched - but with lower confidence reflecting the differences in the image.\n",
    "\n",
    "What if we try to match the original face to a different person?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Get the image to compare\n",
    "img2_url = 'https://raw.githubusercontent.com/MicrosoftLearning/AI-Introduction/master/files/satya.jpg'\n",
    "response2 = requests.get(img2_url)\n",
    "img2 = Image.open(BytesIO(response2.content))\n",
    "\n",
    "# Detect faces in a comparison image\n",
    "result2 = CF.face.detect(img2_url)\n",
    "\n",
    "# Assume the first face is the one we want to compare\n",
    "face2 = result2[0]['faceId']\n",
    "print (\"Face 2:\" + face2)\n",
    "\n",
    "verify_face(face1, face2)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "No match!"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Using the Video Indexer API\n",
    "So far we've used various Cognitive Services APIs to work with static images. However, you can also use the video indexer API to work with video.\n",
    "\n",
    "### Create a Video Indexer account\n",
    "Before you can use the Video Indexer service, you must create a Video Indexer account. In this lab, you will create a free trial account, which has some restrictions on use. If you want to use your account in production, you can link it to your Azure subscription and remove the restrictions.\n",
    "\n",
    "1. Browse to https://www.videoindexer.ai/ and sign in using the Microsoft account associated with your Azure subscription.\n",
    "2. If prompted, allow the app to access your profile information.\n",
    "3. After you have signed into the Video Indexer portal, at the top of the page, next to the **Connect to Azure** button, verify that you can see your account name (which should be derived from your Microsoft account username with some random characters) and the text **Trial** to indicate that this is a trial account.\n",
    "4. Click the dropdown (**&#709;**) symbol for your trial account to display the unique ID associated with the account, which should be a GUID similar to *1a2345bc-d67e-8910-f11g-1213hi14j15k*.\n",
    "5. Copy the account ID, and then paste it in the code below to assign it to the **viAccountID** variable. Then run the code cell to assign the **viLocation** and **viAccountID** variables."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "viLocation = 'trial'\n",
    "viAccountID = 'YOUR_ACCOUNT_ID'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Create a Video Indexer API Subscription\n",
    "At the time of writing, the **Video Indexer** API is in preview, and not available in the Azure portal. To access the preview service, follow these steps:\n",
    "\n",
    "1. Open another browser tab and navigate to https://api-portal.videoindexer.ai/.\n",
    "2. Sign in using the Microsoft account associated with your Azure subscription. \n",
    "3. Select the **Products** tab, and click **Authorization**. You should already have a subscription to this API, so click this. (if not, click **subscribe**).\n",
    "4. View your subscription, and note that primary and secondary keys have been generated for it. The keys should be protected. The keys should only be used by your server code.\n",
    "5. Next to the **Primary key** that has been generated, click **Show**. Then copy and paste the key to set the **viKey** variable in the cell below.\n",
    "6. Run the cell below to assign the variable."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "viKey = 'YOUR_KEY'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now that you have subscribed to the Authorization API, you will be able to obtain access tokens. These access tokens are used to authenticate against the Operations API.\n",
    "\n",
    "Each call to the Operations API should be associated with an access token, matching the authorization scope of the call.\n",
    "\n",
    "- *User* level - user level access tokens let you perform operations on the user level. For example, get associated accounts.\n",
    "- *Account* level – account level access tokens let you perform operations on the account level or the video level. For example, Upload video, list all videos, get video insights, etc.\n",
    "- *Video* level – video level access tokens let you perform operations on a specific video. For example, get video insights, download captions, get widgets, etc.\n",
    "\n",
    "Let's get account level access token using the **Get Account Access Token** method:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import http.client, urllib.request, urllib.parse, urllib.error, base64\n",
    "\n",
    "headers = {\n",
    "    # Request headers\n",
    "    'Ocp-Apim-Subscription-Key': viKey,\n",
    "}\n",
    "\n",
    "params = urllib.parse.urlencode({\n",
    "    # Request parameters\n",
    "    'allowEdit': True,\n",
    "})\n",
    "\n",
    "try:\n",
    "    conn = http.client.HTTPSConnection('api.videoindexer.ai')\n",
    "    conn.request(\"GET\", \"/auth/%s/Accounts/%s/AccessToken?%s\" % (viLocation, viAccountID, params), \"{body}\", headers)\n",
    "    response = conn.getresponse()\n",
    "    data = response.read()\n",
    "    accessToken = data.decode(\"UTF-8\").replace('\"', '')\n",
    "    print(\"accessToken: \" + accessToken)\n",
    "    conn.close()\n",
    "except Exception as e:\n",
    "    print(\"[Errno {0}] {1}\".format(e.errno, e.strerror))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Upload a Video for Processing\n",
    "In this exercise, you will use the **Video Indexer** API to analyze a short video. First, you must upload the video to the Video Indexer so it can be processed. To do this, you can call the **Upload Video** operation, which uploads the video and starts an asynchronous indexing process.\n",
    "\n",
    "Run the cell below to do this."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import http.client, urllib.request, urllib.parse, urllib.error, base64, json\n",
    "\n",
    "# We'll upload this video from GitHub to the Video Indexer\n",
    "video_url='https://github.com/MicrosoftLearning/AI-Introduction/raw/master/files/vid.mp4'\n",
    "\n",
    "headers = {\n",
    "    # Request headers\n",
    "    'Content-Type': 'multipart/form-data',\n",
    "}\n",
    "\n",
    "params = urllib.parse.urlencode({\n",
    "    # Request parameters\n",
    "    'accessToken' : accessToken,\n",
    "    'name': 'vid',\n",
    "    'privacy': 'Private',\n",
    "    'videoUrl': video_url,\n",
    "    'language': 'en-US',\n",
    "})\n",
    "\n",
    "try:\n",
    "    conn = http.client.HTTPSConnection('api.videoindexer.ai')\n",
    "    conn.request(\"POST\", \"/%s/Accounts/%s/Videos?%s\" % (viLocation, viAccountID, params), \"{body}\", headers)\n",
    "    response = conn.getresponse()\n",
    "    data = response.read()\n",
    "    parsed = json.loads(data.decode(\"UTF-8\"))\n",
    "    print(parsed)\n",
    "    conn.close()\n",
    "except Exception as e:\n",
    "    print(e)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The response from the **Upload Video** operation includes an ID for the video breakdown. \n",
    "\n",
    "Let's keep the video id since we will be using this frequently"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "videoID = parsed['id']\n",
    "print(\"videoId: \" + videoID)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Check Processing Status\n",
    "You can use the videoId to track the status of the asynchronous indexing process.\n",
    "\n",
    "Run the following cell to call the **Get Video Index** operation and get the status, and keep running it until the status indicates that the video has been processed."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import http.client, urllib.request, urllib.parse, urllib.error, base64\n",
    "\n",
    "headers = {\n",
    "}\n",
    "\n",
    "params = urllib.parse.urlencode({\n",
    "    # Request parameters\n",
    "    'accessToken': accessToken,\n",
    "    'language': 'en-US',\n",
    "})\n",
    "\n",
    "try:\n",
    "    conn = http.client.HTTPSConnection('api.videoindexer.ai')\n",
    "    conn.request(\"GET\", \"/%s/Accounts/%s/Videos/%s/Index?%s\" % (viLocation, viAccountID, videoID, params), \"{body}\", headers)\n",
    "    response = conn.getresponse()\n",
    "    data = response.read()\n",
    "    parsed = json.loads(data.decode(\"UTF-8\"))\n",
    "    conn.close()\n",
    "except Exception as e:\n",
    "    print(e)\n",
    "\n",
    "print(\"State : \" + parsed['state'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### View the Video\n",
    "The Video Indexer provides a *Player* widget that you can use to embed the video into a web application."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "But in order to access the video, you need a video level access token. This token lets you perform operations on a specific video. For example, get video insights, download captions, get widgets, etc.\n",
    "\n",
    "Let's call the **Get Video Access Token**."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import http.client, urllib.request, urllib.parse, urllib.error, base64\n",
    "\n",
    "headers = {\n",
    "    # Request headers\n",
    "    'Ocp-Apim-Subscription-Key': viKey,\n",
    "}\n",
    "\n",
    "params = urllib.parse.urlencode({\n",
    "    # Request parameters\n",
    "    'allowEdit': True,\n",
    "})\n",
    "\n",
    "try:\n",
    "    conn = http.client.HTTPSConnection('api.videoindexer.ai')\n",
    "    conn.request(\"GET\", \"/auth/%s/Accounts/%s/Videos/%s/AccessToken?%s\" % (viLocation, viAccountID, videoID, params), \"{body}\", headers)\n",
    "    response = conn.getresponse()\n",
    "    data = response.read()\n",
    "    videoAccessToken = data.decode(\"UTF-8\").replace('\"', '')\n",
    "    print(\"videoAccessToken: \" + videoAccessToken)\n",
    "    conn.close()\n",
    "except Exception as e:\n",
    "    print(e)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now, you can use the video access token and run the cell below to watch the video."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from IPython.core.display import HTML\n",
    "\n",
    "playerUrl = \"https://www.videoindexer.ai/embed/player/{0}/{1}/?accessToken={2}\".format(viAccountID,videoID,videoAccessToken)\n",
    "\n",
    "HTML('<iframe width=900 height=600 src=\"%s\"/>' % playerUrl )"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### View the Video Breakdown\n",
    "After the video has been indexed, you can retrieve the detailed breakdown of insights that were found by calling the **Get Video Index** operation.\n",
    "\n",
    "Run the following cell to get the video breakdown in JSON format."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "import http.client, urllib.request, urllib.parse, urllib.error, base64\n",
    "\n",
    "headers = {\n",
    "}\n",
    "\n",
    "params = urllib.parse.urlencode({\n",
    "    # Request parameters\n",
    "    'accessToken': videoAccessToken,\n",
    "    'language': 'English',\n",
    "})\n",
    "\n",
    "try:\n",
    "    conn = http.client.HTTPSConnection('api.videoindexer.ai')\n",
    "    conn.request(\"GET\", \"/%s/Accounts/%s/Videos/%s/Index?%s\" % (viLocation, viAccountID, videoID, params), \"{body}\", headers)\n",
    "    response = conn.getresponse()\n",
    "    data = response.read()\n",
    "    strData = data.decode(\"UTF-8\")\n",
    "    jData = json.loads(strData)\n",
    "    print (json.dumps(jData, sort_keys=True, indent=2))\n",
    "    conn.close()\n",
    "except Exception as e:\n",
    "    print(e)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Get Details of Faces Identified in the Video\n",
    "The breakdown includes details of faces that were identified in the video.\n",
    "\n",
    "Run the following cell to view these details."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": false
   },
   "outputs": [],
   "source": [
    "print(json.dumps(jData[\"summarizedInsights\"][\"faces\"], sort_keys=True, indent=2))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### View a Face Thumbnail\n",
    "In this case, a single unknown face was detected at around 8.4 seconds into the video.\n",
    "\n",
    "Run the following cell to call the **Get Thumbnail** operation and see a thumbnail of the face."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import http.client, urllib.request, urllib.parse, urllib.error, base64\n",
    "from PIL import Image\n",
    "from io import BytesIO\n",
    "from matplotlib.pyplot import imshow\n",
    "%matplotlib inline\n",
    "\n",
    "thumbnailId = jData[\"summarizedInsights\"][\"faces\"][0][\"thumbnailId\"]\n",
    "\n",
    "headers = {\n",
    "}\n",
    "\n",
    "params = urllib.parse.urlencode({\n",
    "    # Request parameters\n",
    "    'accessToken': videoAccessToken,\n",
    "})\n",
    "\n",
    "try:\n",
    "    conn = http.client.HTTPSConnection('api.videoindexer.ai')\n",
    "    conn.request(\"GET\", \"/%s/Accounts/%s/Videos/%s/Thumbnails/%s?%s\" % (viLocation, viAccountID, videoID, thumbnailId, params), \"{body}\", headers)\n",
    "    response = conn.getresponse()\n",
    "    data = response.read()\n",
    "    img = Image.open(BytesIO(data))\n",
    "    imshow(img)\n",
    "    conn.close()\n",
    "except Exception as e:\n",
    "    print(e)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### View (and Edit) People Insights\n",
    "That face looks familiar!\n",
    "You can use the *Insights* widget to allow users to view and edit insights, inclyding those relating to people in the vide.\n",
    "\n",
    "Run the following cell to load the insights widget for people, and then edit the insights to change the name of the person identified to \"Graeme\"."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from IPython.core.display import HTML\n",
    "\n",
    "insightsUrl = \"https://www.videoindexer.ai/embed/insights/{0}/{1}/?accessToken={2}\".format(viAccountID,videoID,videoAccessToken)\n",
    "\n",
    "HTML('<iframe width=900 height=600 src=\"%s\"/>' % insightsUrl )"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Reload Breakdown and Check Updated Face Details\n",
    "To verify that your updates have been saved, run the following cell to reload the breakdown and display the face metadata."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import http.client, urllib.request, urllib.parse, urllib.error, base64\n",
    "\n",
    "headers = {\n",
    "}\n",
    "\n",
    "params = urllib.parse.urlencode({\n",
    "    # Request parameters\n",
    "    'accessToken': videoAccessToken,\n",
    "    'language': 'English',\n",
    "})\n",
    "\n",
    "try:\n",
    "    conn = http.client.HTTPSConnection('api.videoindexer.ai')\n",
    "    conn.request(\"GET\", \"/%s/Accounts/%s/Videos/%s/Index?%s\" % (viLocation, viAccountID, videoID, params), \"{body}\", headers)\n",
    "    response = conn.getresponse()\n",
    "    data = response.read()\n",
    "    strData = data.decode(\"UTF-8\")\n",
    "    jData = json.loads(strData)\n",
    "    print(json.dumps(jData[\"summarizedInsights\"][\"faces\"], sort_keys=True, indent=2))\n",
    "    conn.close()\n",
    "except Exception as e:\n",
    "    print(e)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The name you specified has been assigned to this person, and if this face is detected in any future videos, it will be identified as the same person in this video. "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
