# Allwinner_H616_Devboard
A minimalistic development board designed for the Cortex-A53 Allwinner H616 SoC using KiCad

<p align="center">
     <img height="300" src="https://github.com/Kononenko-K/Allwinner_H616_Devboard/blob/main/pics/main1.png">
     <img height="300" src="https://github.com/Kononenko-K/Allwinner_H616_Devboard/blob/main/pics/main2.png">
</p>

## Overview
The goal of this project, based on the schematics of Orange Pi Zero 2 and Orange Pi Zero 3, was to create a minimalistic development board for the H616 SoC with a functional DDR3/LPDDR4 topology and power supply. This allows it to be used as a basic design that can be modified for specific applications.

## [Hardware](Hardware)
Both versions of the board are powered by the 64-bit 1.5GHz Quad-Core Cortex-A53 Allwinner H616 SoC, supporting either Allwinner H616 or its pin-to-pin compatible successor, Allwinner H618. The primary difference between these chips is the increased L2 cache size in the H618 model.
#### [DDR3 Version:](/Hardware/H616_DDR3)
<p align="center">
     <img width="650" src="https://github.com/Kononenko-K/Allwinner_H616_Devboard/blob/main/pics/2.jpg">
</p>

The DDR3 variant features a compact design optimized for simplicity and ease of learning. Key components include:

- **Memory:** Up to 8 Gbit (1 GB) of BGA-96 16x DDR3 RAM
- **Power Management:** X-Powers AXP305 PMIC
- **Connectivity:** Micro SD slot, USB HS Host connector
- **Communication:** Integrated CP2102 USB-UART converter

#### [LPDDR4 Version:](/Hardware/H616_LPDDR4)
<p align="center">
     <img width="650" src="https://github.com/Kononenko-K/Allwinner_H616_Devboard/blob/main/pics/3.jpg">
</p>

The LPDDR4 variant offers enhanced capabilities tailored for my specific application, while also remaining suitable for educational use:

- **Memory:** Up to 32 Gbit (4 GB) of BGA-200 32x LPDDR4 RAM
- **Power Management:** X-Powers AXP313A PMIC
- **Storage:** Integrated SD2.0 Flash Memory chip and MicroSD slot for flexible storage options
- **Auxiliary Processing:** Cortex-M4 STM32 microcontroller for additional processing tasks
- **Communication:** Integrated CP2102 USB-UART converter

To power the board via USB and connect external devices, a custom [USB board adapter](/Hardware/Debug_Adapter) is available.

### **Manufacturing specifications:**
- **Layers:** 4-layer design  
- **Trace/Space:** 3.5/3.5 mil  
- **Via Sizes:** 0.35/0.15 mm 
- **Prepreg:** 80u  

There are PDF documents available for both [DDR3](/Hardware/H616_DDR3/project.pdf) and [LPDDR4](/Hardware/H616_LPDDR4/project.pdf) versions.

## Software

### **Building from Mainline:**
#### Arm Trusted Firmware (TF-A):
- Source: [here](https://git.trustedfirmware.org/TF-A/trusted-firmware-a.git/)
```sh
make CROSS_COMPILE=aarch64-linux-gnu- PLAT=sun50i_h616 RESET_TO_BL31=1
```
After building, copy the `bl31.bin` file to the U-Boot sources directory.

#### U-Boot:
- Source: [here](https://github.com/u-boot/u-boot)
```sh
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- orangepi_zero2_defconfig
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- BL31=bl31.bin
```

#### Linux Kernel:
- Source: [www.kernel.org](http://www.kernel.org)
```sh
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- defconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- Image modules dtbs
```

#### Rootfs:
Example sources for arm64 rootfs:
- [rcn-ee.com](https://rcn-ee.com/rootfs/eewiki/minfs)
- [Linaro.org](https://releases.linaro.org/openembedded/images/)

#### Preparing SD Card:
1. Create two partitions: a small fat32 for boot files and an ext4 for rootfs.
2. Write U-Boot to the card:
```sh
sudo dd if=/dev/zero of=/dev/mmcblk0 bs=1k count=1023 seek=1
sudo dd if=u-boot-sunxi-with-spl.bin of=/dev/mmcblk0 bs=1024 seek=8
```
3. Copy dtb and kernel image to the first partition, then unpack rootfs to the second.

If you prefer to load U-Boot into RAM and execute it directly over USB without using an SD card, you can use the `sunxi-fel` utility:  
   ```sh
   sudo sunxi-fel uboot u-boot-sunxi-with-spl.bin
   ```  
This method is useful for testing or when bypassing the SD card for some reason.

#### Booting from U-Boot:
Enter these commands in the U-Boot console:
```sh
setenv bootargs console=ttyS0,115200 root=/dev/mmcblk0p2 rw rootwait
setenv bootcmd "mmc rescan; fatload mmc 0:1 0x46000000 Image; fatload mmc 0:1 0x49000000 sun50i-h616-orangepi-zero2.dtb; booti 0x46000000 - 0x49000000"
```
Use a `boot.scr` file for automatic booting.

### **Using Buildroot:**
For LPDDR4 version:
```sh
make orangepi_zero3_defconfig
```
For DDR3 versions, modify the config:
```sh
BR2_LINUX_KERNEL_INTREE_DTS_NAME="allwinner/sun50i-h616-orangepi-zero2.dts"
BR2_TARGET_UBOOT_BOARD_DEFCONFIG="orangepi_zero2"
```
Download sources with `make source`, then build.

## License
- The **Hardware** in this project is licensed under the [CERN Open Hardware Licence Permissive (CERN OHL-P)](LICENSE).