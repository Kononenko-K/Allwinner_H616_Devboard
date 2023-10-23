# Allwinner_H616_Devboard
A bare minimum development board for Cortex-A53 Allwinner H616 SoC made with KiCad

<p align="center">
     <img width="900" src="https://github.com/Kononenko-K/Allwinner_H616_Devboard/blob/main/pics/main.png">
</p>

## Overview
The goal of this project was to make a minimalistic design for H616 SoC with working DDR3 topology and power supply, so that it can be used as a basic design that can be modified for any specific application of this SoC.
The devboard is basically combatible with all Orange Pi Zero 2 distros. Alternatively, you can build u-boot and the linux kernel on your own (assuming you've installed a proper cross compilation toolchain and all required dependencies).

## [Hardware](Hardware)
<p align="center">
     <img width="800" src="https://github.com/Kononenko-K/Allwinner_H616_Devboard/blob/main/pics/2.jpg">
</p>

The board features 64-bit 1.5GHz Quad-Core Cortex-A53 Allwinner H616 SOC, up to 8 Gbit (1 GB) of BGA-90 16x DDR3 RAM, Micro SD slot, USB HS Host connector and integrated CP2102 USB-UART converter. 4 layers; 3,5/3,5 mil; 0,35/0,15 via, 80u prepreg.
There are [KiCad project](/Hardware), [Gerber files](/Hardware/gerber) and [PDF](/Hardware/project.pdf) avaliable.

## Software
Here is a brief guide through building U-Boot and the Linux kernel for this board from mainline.

### Building Arm Trusted Firmware:
TF-A source code could be taken from [here](https://git.trustedfirmware.org/TF-A/trusted-firmware-a.git/).
```sh
make CROSS_COMPILE=aarch64-linux-gnu- PLAT=sun50i_h616 RESET_TO_BL31=1
```

After that copy bl31.bin file from ../build/sun50i_h616/release to the U-Boot sources root directory.

### Building U-Boot:
Download sources from [here](https://github.com/u-boot/u-boot), then do:
```sh
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- orangepi_zero2_defconfig
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- BL31=bl31.bin
```
### Building the Linux kernel:
Download and extract sources from [here](www.kernel.org), then execute:
```sh
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- defconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- Image modules dtbs
```
### Rootfs:
Builded rootfs for arm64 could be taken for example from [here](https://rcn-ee.com/rootfs/eewiki/minfs) or [here](https://releases.linaro.org/openembedded/images/).

### Preparing SD-Card:
Make two partitions. A small fat32 one for dtb file and the kernel image, and a larger one in ext4 for rootfs.
Then clean the partition table and write u-boot on it:
```sh
sudo dd if=/dev/zero of=/dev/mmcblk0 bs=1k count=1023 seek=1
sudo dd if=u-boot-sunxi-with-spl.bin of=/dev/mmcblk0 bs=1024 seek=8
```
After that, copy dtb file and kernel image to the first partition, and unpack rootfs to the second one. 

### Booting from U-Boot
The system can be booted by typing next cmds to the command line in U-Boot:
```sh
setenv bootargs console=ttyS0,115200 root=/dev/mmcblk0p2 rw rootwait
setenv bootcmd `mmc rescan; fatload mmc 0:1 0x46000000 Image; fatload mmc 0:1 0x49000000 sun50i-h616-orangepi-zero2.dtb; booti 0x46000000 - 0x49000000`
```
Then you shoud use a proper boot.scr file to boot the system automatically.
