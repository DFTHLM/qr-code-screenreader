# Notes about QR codes

- ## Error correction levels:
    - **Low**      |0|0| (0) - **7%** error correction, takes up about **25 to 35%** of the data space
    - **Medium**   |1|0| (1) - **15%** error correction, takes up about **35 to 50%** of the data space
    - **Quartile** |0|1| (2) - **25%** error correction, takes up about **50 to 65%** of the data space
    - **High**     |1|1| (3) - **30%** error correction, takes up about **60 to 70%** of the data space

### Error correction is with Reed-Solomon codewords:
1. Data is stored into *data codewords* - 8 bits
2. If needed, data is split into *blocks*, each block is treated *separately*
3. Using *modulo operations over finite fields*, ECC codewords are generated
4. The data is *interleaved* with the ECC codewords

### Reed-Solomon in details:

- ## Data encoding modes:
    - **Numeric**      |0|0|0|0| (0) - 0-9, 10 bits per 3 digits
    - **Alphanumeric** |0|0|0|1| (1) - 0-9, A-Z, space, $, %, *, +, -, ., /, :, 11 bits per 2 characters
    - **Byte**         |0|0|1|0| (2) - 8 bit binary data, 8 bits per character
    - **Kanji**        |0|0|1|1| (3) - Shift JIS encoding, 13 bits per character

- ## Masks:
    - |0|0|0| (0) => (i + j) % 2 == 0
    - |0|1|0| (1) => i % 2 == 0
    - |0|0|1| (2) => j % 3 == 0
    - |0|1|1| (3) => (i + j) % 3 == 0
    - |1|0|0| (4) => (i // 2 + j // 3) % 2 == 0
    - |1|0|1| (5) => ((i * j) % 2 + (i * j) % 3) == 0
    - |1|1|0| (6) => ((i + j) % 2 + (i * j) % 3) == 0
    - |1|1|1| (7) => ((i * j) % 3 + (i + j) % 2) == 0

- masks are applied with *XOR*
- mask info is *raw*, stored around the finder patterns except in places where the version info is stored

<img src="https://www.kindpng.com/picc/m/461-4614753_qr-code-mask-pattern-hd-png-download.png"/>

## QR code versions:
- *finders* are always *7x7*, in the corners, and there are always 3
- *alignment patterns* are *5x5*, and there are up to 7 in total, starting at version 2
- *version info* is *18 bits*, and is in the top right and bottom left corner, on the side of the finder pattern facing the top left one

## Additional info:
- *timing patterns* are 1 high strips going from bottom right corner of the top left finder to the edges of the other 2 finders in a straight line
- *timing patterns* alternate between 1 and 0 (white and black)
- quiet zone is *4 wide*
- data is stored in a *zigzag pattern*, starting from the bottom right corner of the qr code

## QRcode anatomy:
<img src="https://www.shieldui.com/sites/default/files/blogs/QRStructure123.png"/>
