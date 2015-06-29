# dup-image-search
This project is to help the Internet Archive find duplicate images for their many images (particularly music album art covers).

## Algorithms used
Thanks to http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html for the Simple Hash and pHash (aka perceptive hash, which uses DCT)

<ul>
<li>MD5 checksum (This may change to SHA.)</li>
<li>Simple Hash<br>Scale to 8x8, greyscale, hash based on above/below average</li>
<li>DCT (Discrete Cosine Tranform)<br>Scale to 32x32, greyscale, [DCT](https://en.wikipedia.org/wiki/Discrete_cosine_transform), hash based on above/below average excluding top-left "base" value</li>
</ul>
