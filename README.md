# 🛠️ ESP3D Portfolio

<div align="center">

![Repositories](https://img.shields.io/badge/Repositories-14-blue)
![Main Projects](https://img.shields.io/badge/Main%20Projects-8-orange)
![Dependencies](https://img.shields.io/badge/Dependencies-6-green)
![Open Issues](https://img.shields.io/badge/Open%20Issues-39-yellow)
![Last Update](https://img.shields.io/badge/Last%20Update-2026%20%2F%2001%20%2F%2019%2001:23%20UTC-lightgrey)

📑 Real-time status and analysis of ESP3D-related projects

</div>

## 🔍 Quick Navigation

<div align="center">

| Section | Type | Version | Description |
|---------|------|---------|-------------|
| [⭐ ESP3D](#user-content-esp3d) | Main Project | v3.0.1 / dev:3.0.2 | FW for ESP8266/ESP8285/ESP32 used with 3D printer |
| [⭐ ESP3DLib](#user-content-esp3dlib) | Main Project | v1.0.0 | ESP3D library for Marlin and ESP32 boards |
| [⭐ ESP3D-WEBUI](#user-content-esp3d-webui) | Main Project | v3.0.1 / dev:3.0.2 | A Web UI for ESP8266 or ESP32 based boards connected to 3D printers / CNC |
| [⭐ ESP3D-TFT](#user-content-esp3d-tft) | Main Project | v3.0.0.a26 | ESP3D Firmware for ESP32 based TFT  |
| [⭐ Marlin](#user-content-marlin) | Main Project | missing | Marlin is an optimized firmware for RepRap 3D printers based on the Arduino platform. | Many commercial 3D printers come with Marlin installed. Check with your vendor if you need source code for your specific machine. |
| [⭐ ESP3D-Configurator](#user-content-esp3d-configurator) | Main Project | v1.0.34 | Configurator for ESP3D Firmware |
| [⭐ esp3d.io](#user-content-esp3d.io) | Main Project | v2.1.0 | Documentation of ESP3D Ecosystem |
| [⭐ esp3d-webinstaller](#user-content-esp3d-webinstaller) | Main Project | v1.0.0 / dev:1.0.2 | Web Installer for ESP32 projects |
| [🔗 ESP32SSDP](#user-content-esp32ssdp) | Dependency | v2.0.4 | Simple SSDP library for ESP32 |
| [🔗 SSDP_IDF](#user-content-ssdp_idf) | Dependency | v1.0.0 | SSDP IDF component for ESP32 |
| [🔗 esp32-usb-serial](#user-content-esp32-usb-serial) | Dependency | v1.0.1 | Arduino Library to use USB as OTG on ESP32 capable devices based on espressif IDF components |
| [🔗 EspLuaEngine](#user-content-espluaengine) | Dependency | v1.0.3 | Add Lua engine to your firmware using ESP boards |
| [🔗 plugin_oled_display](#user-content-plugin_oled_display) | Dependency | v1.0.1 | grblHAL plugin for oled display |
| [📋 Global Issues](#-global-issues) | Overview | - | All open issues across projects |
| [📊 Statistics](#-statistics) | Metrics | - | Project health and activity metrics |

</div>

## 📊 Activity Rankings

Repository activity rankings based on activity over different time periods.

### Last 24 Hours

<div class="activity-ranking">

| Rank &nbsp; | Repository | Type | Score | Commits | Issues | Activity/Day |
|:------------|------------|------|--------|---------|---------|-------------|
| 🥇 1  | Private Project #1 | Private | 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦 (18) | 6 | 0 | 18.0 |
| 🥈 2  | [ESP3D](https://github.com/luc-github/ESP3D) | Main | 🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜ (2) | 0 | 1 | 2.0 |
| 🥉 3  | [ESP3D-WEBUI](https://github.com/luc-github/ESP3D-WEBUI) | Main | 🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜ (2) | 0 | 1 | 2.0 |
| ▪️ 4  | [ESP3DLib](https://github.com/luc-github/ESP3DLib) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 5  | [ESP3D-TFT](https://github.com/luc-github/ESP3D-TFT) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 6  | [Marlin](https://github.com/luc-github/Marlin) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 7  | [ESP3D-Configurator](https://github.com/luc-github/ESP3D-Configurator) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 8  | [esp3d.io](https://github.com/luc-github/esp3d.io) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 9  | [esp3d-webinstaller](https://github.com/luc-github/esp3d-webinstaller) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 10 | [ESP32SSDP](https://github.com/luc-github/ESP32SSDP) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 11 | [SSDP_IDF](https://github.com/luc-github/SSDP_IDF) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 12 | [esp32-usb-serial](https://github.com/luc-github/esp32-usb-serial) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 13 | [EspLuaEngine](https://github.com/luc-github/EspLuaEngine) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 14 | [plugin_oled_display](https://github.com/luc-github/plugin_oled_display) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |

</div>

### Last 7 Days

<div class="activity-ranking">

| Rank &nbsp; | Repository | Type | Score | Commits | Issues | Activity/Day |
|:------------|------------|------|--------|---------|---------|-------------|
| 🥇 1  | Private Project #1 | Private | 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦 (63) | 21 | 0 | 9.0 |
| 🥈 2  | [ESP3D](https://github.com/luc-github/ESP3D) | Main | 🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜ (11) | 3 | 1 | 1.6 |
| 🥉 3  | [ESP3D-WEBUI](https://github.com/luc-github/ESP3D-WEBUI) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (4) | 0 | 2 | 0.6 |
| ▪️ 4  | [ESP3D-TFT](https://github.com/luc-github/ESP3D-TFT) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (2) | 0 | 1 | 0.3 |
| ▪️ 5  | [ESP3DLib](https://github.com/luc-github/ESP3DLib) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 6  | [Marlin](https://github.com/luc-github/Marlin) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 7  | [ESP3D-Configurator](https://github.com/luc-github/ESP3D-Configurator) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 8  | [esp3d.io](https://github.com/luc-github/esp3d.io) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 9  | [esp3d-webinstaller](https://github.com/luc-github/esp3d-webinstaller) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 10 | [ESP32SSDP](https://github.com/luc-github/ESP32SSDP) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 11 | [SSDP_IDF](https://github.com/luc-github/SSDP_IDF) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 12 | [esp32-usb-serial](https://github.com/luc-github/esp32-usb-serial) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 13 | [EspLuaEngine](https://github.com/luc-github/EspLuaEngine) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 14 | [plugin_oled_display](https://github.com/luc-github/plugin_oled_display) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |

</div>

### Last 30 Days

<div class="activity-ranking">

| Rank &nbsp; | Repository | Type | Score | Commits | Issues | Activity/Day |
|:------------|------------|------|--------|---------|---------|-------------|
| 🥇 1  | Private Project #1 | Private | 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦 (162) | 54 | 0 | 5.4 |
| 🥈 2  | [ESP3D](https://github.com/luc-github/ESP3D) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (11) | 3 | 1 | 0.4 |
| 🥉 3  | [ESP3D-WEBUI](https://github.com/luc-github/ESP3D-WEBUI) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (6) | 0 | 3 | 0.2 |
| ▪️ 4  | [ESP3D-TFT](https://github.com/luc-github/ESP3D-TFT) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (2) | 0 | 1 | 0.1 |
| ▪️ 5  | [ESP3DLib](https://github.com/luc-github/ESP3DLib) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 6  | [Marlin](https://github.com/luc-github/Marlin) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 7  | [ESP3D-Configurator](https://github.com/luc-github/ESP3D-Configurator) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 8  | [esp3d.io](https://github.com/luc-github/esp3d.io) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 9  | [esp3d-webinstaller](https://github.com/luc-github/esp3d-webinstaller) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 10 | [ESP32SSDP](https://github.com/luc-github/ESP32SSDP) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 11 | [SSDP_IDF](https://github.com/luc-github/SSDP_IDF) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 12 | [esp32-usb-serial](https://github.com/luc-github/esp32-usb-serial) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 13 | [EspLuaEngine](https://github.com/luc-github/EspLuaEngine) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |
| ▪️ 14 | [plugin_oled_display](https://github.com/luc-github/plugin_oled_display) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |

</div>

### Last 365 Days

<div class="activity-ranking">

| Rank &nbsp; | Repository | Type | Score | Commits | Issues | Activity/Day |
|:------------|------------|------|--------|---------|---------|-------------|
| 🥇 1  | Private Project #1 | Private | 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦 (162) | 54 | 0 | 0.4 |
| 🥈 2  | [ESP3D](https://github.com/luc-github/ESP3D) | Main | 🟦🟦🟦🟦🟦🟦🟦⬜⬜⬜ (114) | 36 | 3 | 0.3 |
| 🥉 3  | [plugin_oled_display](https://github.com/luc-github/plugin_oled_display) | Dependency | 🟦🟦🟦🟦🟦🟦⬜⬜⬜⬜ (99) | 33 | 0 | 0.3 |
| ▪️ 4  | [esp3d-webinstaller](https://github.com/luc-github/esp3d-webinstaller) | Main | 🟦🟦🟦🟦⬜⬜⬜⬜⬜⬜ (78) | 26 | 0 | 0.2 |
| ▪️ 5  | [ESP3D-WEBUI](https://github.com/luc-github/ESP3D-WEBUI) | Main | 🟦🟦🟦🟦⬜⬜⬜⬜⬜⬜ (75) | 21 | 6 | 0.2 |
| ▪️ 6  | [esp3d.io](https://github.com/luc-github/esp3d.io) | Main | 🟦🟦⬜⬜⬜⬜⬜⬜⬜⬜ (38) | 12 | 1 | 0.1 |
| ▪️ 7  | [ESP3DLib](https://github.com/luc-github/ESP3DLib) | Main | 🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜ (29) | 9 | 1 | 0.1 |
| ▪️ 8  | [ESP3D-TFT](https://github.com/luc-github/ESP3D-TFT) | Main | 🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜ (24) | 6 | 3 | 0.1 |
| ▪️ 9  | [ESP32SSDP](https://github.com/luc-github/ESP32SSDP) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (11) | 3 | 1 | 0.0 |
| ▪️ 10 | [esp32-usb-serial](https://github.com/luc-github/esp32-usb-serial) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (9) | 3 | 0 | 0.0 |
| ▪️ 11 | [ESP3D-Configurator](https://github.com/luc-github/ESP3D-Configurator) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (8) | 2 | 1 | 0.0 |
| ▪️ 12 | [SSDP_IDF](https://github.com/luc-github/SSDP_IDF) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (6) | 2 | 0 | 0.0 |
| ▪️ 13 | [EspLuaEngine](https://github.com/luc-github/EspLuaEngine) | Dependency | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (6) | 2 | 0 | 0.0 |
| ▪️ 14 | [Marlin](https://github.com/luc-github/Marlin) | Main | ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (0) | 0 | 0 | 0.0 |

</div>

### Legend

- 🟦 Activity Score relative to most active repository
- Score = (Commits × 3) + (Issues × 2) + (Comments × 1)
- Activity/Day = Average daily activity score for the period
- Higher scores indicate more activity

## ⭐ Popularity Rankings

Repository popularity based on GitHub stars and forks.

<div class="popularity-ranking">

| Rank &nbsp; | Repository | Type | ⭐ Stars | 🍴 Forks | 👀 Watchers |
|:------------|------------|------|---------|---------|-------------|
| 🥇 1  | [ESP3D](https://github.com/luc-github/ESP3D) | Main | 1,939 | 486 | 1,939 |
| 🥈 2  | [ESP3D-WEBUI](https://github.com/luc-github/ESP3D-WEBUI) | Main | 859 | 338 | 859 |
| 🥉 3  | [ESP3DLib](https://github.com/luc-github/ESP3DLib) | Main | 115 | 35 | 115 |
| ▪️ 4  | [ESP32SSDP](https://github.com/luc-github/ESP32SSDP) | Dependency | 54 | 27 | 54 |
| ▪️ 5  | [ESP3D-TFT](https://github.com/luc-github/ESP3D-TFT) | Main | 49 | 14 | 49 |
| ▪️ 6  | [esp32-usb-serial](https://github.com/luc-github/esp32-usb-serial) | Dependency | 18 | 5 | 18 |
| ▪️ 7  | [esp3d.io](https://github.com/luc-github/esp3d.io) | Main | 11 | 62 | 11 |
| ▪️ 8  | [Marlin](https://github.com/luc-github/Marlin) | Main | 9 | 5 | 9 |
| ▪️ 9  | [ESP3D-Configurator](https://github.com/luc-github/ESP3D-Configurator) | Main | 9 | 5 | 9 |
| ▪️ 10 | [SSDP_IDF](https://github.com/luc-github/SSDP_IDF) | Dependency | 3 | 3 | 3 |
| ▪️ 11 | [EspLuaEngine](https://github.com/luc-github/EspLuaEngine) | Dependency | 3 | 1 | 3 |
| ▪️ 12 | [esp3d-webinstaller](https://github.com/luc-github/esp3d-webinstaller) | Main | 2 | 0 | 2 |
| ▪️ 13 | [plugin_oled_display](https://github.com/luc-github/plugin_oled_display) | Dependency | 2 | 0 | 2 |

</div>

## 📊 Statistics

<details>
<summary>Click to view detailed statistics</summary>

### Repository Statistics

| Metric | Value |
|--------|-------|
| Total Repositories | 14 |
| Main Projects | 8 |
| Dependencies | 6 |
| Total Stars | 3073 |
| Total Forks | 981 |

### Issue Statistics

| Metric | Value |
|--------|-------|
| Open Issues | 39 |
| Closed Issues | 0 |
| Average Age | 933.9 days |
| Close Rate | 0.0% |

### Recent Activity

```
Commit Activity:

Daily    🟦 Few (1-2 commits)            (0.4 commits)
Weekly   🟦 Few (1-10 commits)           (2.8 commits)
Monthly  🟦 Few (1-25 commits)           (11.4 commits)
```

</details>

## 📦 Projects Status

<details open id="esp3d">
<summary><h3>⭐ ESP3D</h3></summary>
<table><tr><td>

**Project**: [ESP3D](https://github.com/luc-github/ESP3D)<br>
**Type**: Main<br>
**Version**: 🔵 v3.0.1 / dev:3.0.2<br>
**Description**: FW for ESP8266/ESP8285/ESP32 used with 3D printer<br>
**Language**: C<br>
**Health Score**: <span style="color: #ff0000">32.5%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`3.0`)</h4></summary>

```
Last commit: 2026-01-15 (#693f31f)
Author: Luc
```

<table>
<tr><th>Status</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>#1116: <a href="https://github.com/luc-github/ESP3D/issues/1116">websocket connection error</a></td><td><code>2026-01-18</code></td><td><code>2026-01-19</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#243: <a href="https://github.com/luc-github/ESP3D/issues/243">[FEATURE REQUEST]🦄GCODE Streamer Host definition for 3.X</a></td><td><code>2018-07-14</code></td><td><code>2025-12-08</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#795: <a href="https://github.com/luc-github/ESP3D/issues/795">[TODO]☑Code refactoring plan</a></td><td><code>2022-07-28</code></td><td><code>2025-03-26</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#568: <a href="https://github.com/luc-github/ESP3D/issues/568">[FEATURE REQUEST]🦄USB Disk support using CH376S chip</a></td><td><code>2021-01-24</code></td><td><code>2024-10-28</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#575: <a href="https://github.com/luc-github/ESP3D/issues/575">⏸️[FEATURE REQUEST]🦄Use better serial protocol communication</a></td><td><code>2021-02-01</code></td><td><code>2024-03-06</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

</details>

<hr>

<details open id="esp3d-configurator">
<summary><h3>⭐ ESP3D-Configurator</h3></summary>
<table><tr><td>

**Project**: [ESP3D-Configurator](https://github.com/luc-github/ESP3D-Configurator)<br>
**Type**: Main<br>
**Version**: 🟢 v1.0.34<br>
**Description**: Configurator for ESP3D Firmware<br>
**Language**: JavaScript<br>
**Health Score**: <span style="color: #ff0000">24.4%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`main`)</h4></summary>

```
Last commit: 2025-12-17 (#644f37a)
Author: Luc
```

<table>
<tr><th>Status</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>#28: <a href="https://github.com/luc-github/ESP3D-Configurator/issues/28">[FEATURE REQUEST] Configure Client mode</a></td><td><code>2025-03-10</code></td><td><code>2025-03-10</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#16: <a href="https://github.com/luc-github/ESP3D-Configurator/issues/16">[FEATURE REQUEST]Web Flasher Tool</a></td><td><code>2023-05-18</code></td><td><code>2023-05-18</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#5: <a href="https://github.com/luc-github/ESP3D-Configurator/issues/5">[Information]Devt status</a></td><td><code>2022-06-18</code></td><td><code>2022-08-18</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

</details>

<hr>

<details open id="esp3d-tft">
<summary><h3>⭐ ESP3D-TFT</h3></summary>
<table><tr><td>

**Project**: [ESP3D-TFT](https://github.com/luc-github/ESP3D-TFT)<br>
**Type**: Main<br>
**Version**: 🟢 v3.0.0.a26<br>
**Description**: ESP3D Firmware for ESP32 based TFT <br>
**Language**: C<br>
**Health Score**: <span style="color: #ff0000">25.5%</span>

</td></tr></table>

<details>
<summary><h4>🔧 Development Branch (`main`)</h4></summary>

```
Last commit: 2025-12-17 (#48c6ef0)
Author: Luc
```

<table>
<tr><th>Status</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>#82: <a href="https://github.com/luc-github/ESP3D-TFT/issues/82">[FEATURE REQUEST] Support for MKS DLC32 MAX LCD [ESP-TFT35 v4.1]</a></td><td><code>2025-12-28</code></td><td><code>2026-01-17</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#81: <a href="https://github.com/luc-github/ESP3D-TFT/issues/81">The serial port cannot be connected to the printer, but the USB serial port can</a></td><td><code>2025-05-19</code></td><td><code>2025-07-29</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#54: <a href="https://github.com/luc-github/ESP3D-TFT/issues/54">[FEATURE REQUEST]Move to lvgl 9.0</a></td><td><code>2024-01-17</code></td><td><code>2025-05-08</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#55: <a href="https://github.com/luc-github/ESP3D-TFT/issues/55">[FEATURE REQUEST]Code review / refactoring / improvement</a></td><td><code>2024-01-19</code></td><td><code>2024-12-14</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#76: <a href="https://github.com/luc-github/ESP3D-TFT/issues/76">[FEATURE REQUEST]Add Lua interpreter support like in ESP3D</a></td><td><code>2024-10-13</code></td><td><code>2024-10-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#74: <a href="https://github.com/luc-github/ESP3D-TFT/issues/74">[FEATURE REQUEST]Add BTT GCODE thumbnails</a></td><td><code>2024-08-14</code></td><td><code>2024-08-14</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#67: <a href="https://github.com/luc-github/ESP3D-TFT/issues/67">[FEATURE REQUEST]Add support of macro defined by webui on screen</a></td><td><code>2024-04-21</code></td><td><code>2024-08-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#53: <a href="https://github.com/luc-github/ESP3D-TFT/issues/53">[FEATURE REQUEST]Do better snapshot code with no memory need</a></td><td><code>2024-01-07</code></td><td><code>2024-01-07</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#12: <a href="https://github.com/luc-github/ESP3D-TFT/issues/12">[FEATURE REQUEST]WhatsApp Notification</a></td><td><code>2023-02-20</code></td><td><code>2023-02-20</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#5: <a href="https://github.com/luc-github/ESP3D-TFT/issues/5">[ENHANCEMENT]Add Pin interrupt support on FT5X06 when supported to save mcu time instead of doing permanent polling</a></td><td><code>2022-10-01</code></td><td><code>2022-10-01</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

</details>

<hr>

<details open id="esp3d-webinstaller">
<summary><h3>⭐ esp3d-webinstaller</h3></summary>
<table><tr><td>

**Project**: [esp3d-webinstaller](https://github.com/luc-github/esp3d-webinstaller)<br>
**Type**: Main<br>
**Version**: 🔵 v1.0.0 / dev:1.0.2<br>
**Description**: Web Installer for ESP32 projects<br>
**Language**: JavaScript<br>
**Health Score**: <span style="color: #ff0000">19.0%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`main`)</h4></summary>

```
Last commit: 2025-12-17 (#f738bac)
Author: Luc
```

> 🎉 No open issues

</details>

</details>

<hr>

<details open id="esp3d-webui">
<summary><h3>⭐ ESP3D-WEBUI</h3></summary>
<table><tr><td>

**Project**: [ESP3D-WEBUI](https://github.com/luc-github/ESP3D-WEBUI)<br>
**Type**: Main<br>
**Version**: 🔵 v3.0.1 / dev:3.0.2<br>
**Description**: A Web UI for ESP8266 or ESP32 based boards connected to 3D printers / CNC<br>
**Language**: JavaScript<br>
**Health Score**: <span style="color: #ff0000">25.5%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`3.0`)</h4></summary>

```
Last commit: 2025-12-17 (#338d4b8)
Author: Luc
```

<table>
<tr><th>Status</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>#438: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/438">Adding a custom logo</a></td><td><code>2025-12-28</code></td><td><code>2026-01-19</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#390: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/390">[FEATURE REQUEST]Port surfacing wizard as extension </a></td><td><code>2024-06-02</code></td><td><code>2026-01-14</code></td><td style="color: #000000">normal</td></tr>
<tr><td>🔄</td><td>#439: <a href="https://github.com/luc-github/ESP3D-WEBUI/pull/439">Bump qs and express</a></td><td><code>2025-12-30</code></td><td><code>2025-12-30</code></td><td style="color: #000000">normal</td></tr>
<tr><td>🔄</td><td>#418: <a href="https://github.com/luc-github/ESP3D-WEBUI/pull/418">Updated to 2.1.3c0 version</a></td><td><code>2025-09-20</code></td><td><code>2025-09-23</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#414: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/414">[FEATURE REQUEST]Add filament runout sensor status to WEB UI</a></td><td><code>2025-08-31</code></td><td><code>2025-09-01</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#411: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/411">[FEATURE REQUEST] Flexible panels customizations to optimize empty space</a></td><td><code>2025-03-30</code></td><td><code>2025-03-30</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#244: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/244">CNC process visualization functionality</a></td><td><code>2022-05-14</code></td><td><code>2024-11-25</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#122: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/122">[FEATURE REQUEST]PCB and Engraving Milling autoleveling</a></td><td><code>2020-10-10</code></td><td><code>2024-10-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#106: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/106">[FEATURE REQUEST] Bed Mesh Leveling Visualizer</a></td><td><code>2020-07-22</code></td><td><code>2024-10-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#265: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/265">[FEATURE REQUEST]Integrate the [ ESP700] command into the button</a></td><td><code>2022-09-18</code></td><td><code>2024-10-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#85: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/85">[FEATURE REQUEST]Be able to autodiscover all ESP3D devices and agregate them</a></td><td><code>2020-01-04</code></td><td><code>2022-08-15</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#242: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/242">[FEATURE REQUEST]Configuration  Wizard </a></td><td><code>2022-05-10</code></td><td><code>2022-06-06</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

</details>

<hr>

<details open id="esp3d.io">
<summary><h3>⭐ esp3d.io</h3></summary>
<table><tr><td>

**Project**: [esp3d.io](https://github.com/luc-github/esp3d.io)<br>
**Type**: Main<br>
**Version**: 🟢 v2.1.0<br>
**Description**: Documentation of ESP3D Ecosystem<br>
**Language**: HTML<br>
**Health Score**: <span style="color: #ff0000">24.6%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`main`)</h4></summary>

```
Last commit: 2025-12-17 (#759f2d9)
Author: Luc
```

<table>
<tr><th>Status</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>#49: <a href="https://github.com/luc-github/esp3d.io/issues/49">List external devices  tested / supported by ESP3D</a></td><td><code>2025-02-26</code></td><td><code>2025-02-26</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#8: <a href="https://github.com/luc-github/esp3d.io/issues/8">Do a description page for each WebUI panel / Settings</a></td><td><code>2023-02-28</code></td><td><code>2023-02-28</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#6: <a href="https://github.com/luc-github/esp3d.io/issues/6">Add Default setting description page</a></td><td><code>2023-02-28</code></td><td><code>2023-02-28</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

</details>

<hr>

<details open id="esp3dlib">
<summary><h3>⭐ ESP3DLib</h3></summary>
<table><tr><td>

**Project**: [ESP3DLib](https://github.com/luc-github/ESP3DLib)<br>
**Type**: Main<br>
**Version**: 🟢 v1.0.0<br>
**Description**: ESP3D library for Marlin and ESP32 boards<br>
**Language**: C++<br>
**Health Score**: <span style="color: #ff0000">25.5%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`master`)</h4></summary>

```
Last commit: 2025-12-17 (#515c62d)
Author: Luc
```

> 🎉 No open issues

</details>

<details>
<summary><h4>🔧 Development Branch (`3.0`)</h4></summary>

```
Last commit: 2023-10-05 (#b5c99e2)
Author: Luc
```

<table>
<tr><th>Status</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>#87: <a href="https://github.com/luc-github/ESP3DLib/issues/87">[Compatibility issue]SDFat library  in ESP3D 3.0 conflict with latest Marlin SD implementation</a></td><td><code>2025-03-22</code></td><td><code>2025-03-22</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#39: <a href="https://github.com/luc-github/ESP3DLib/issues/39">[FEATURE REQUEST]ESP3DLib 3.0</a></td><td><code>2022-02-01</code></td><td><code>2024-12-21</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

</details>

<hr>

<details open id="marlin">
<summary><h3>⭐ Marlin</h3></summary>
<table><tr><td>

**Project**: [Marlin](https://github.com/luc-github/Marlin)<br>
**Type**: Main<br>
**Version**: ⚪ missing<br>
**Description**: Marlin is an optimized firmware for RepRap 3D printers based on the Arduino platform. | Many commercial 3D printers come with Marlin installed. Check with your vendor if you need source code for your specific machine.<br>
**Language**: C++<br>
**Health Score**: <span style="color: #ff0000">13.9%</span>

</td></tr></table>

<details>
<summary><h4>🔧 Development Branch (`ESP3DLib-V3-bugfix-2.1.x`)</h4></summary>

```
Last commit: 2024-03-21 (#9d9f72b)
Author: Luc
```

> 🎉 No open issues

</details>

<details>
<summary><h4>🔧 Development Branch (`ESP3DLib-V3-2.1.2`)</h4></summary>

```
Last commit: 2024-03-23 (#635d22c)
Author: Luc
```

> 🎉 No open issues

</details>

</details>

<hr>

<details open id="esp32-usb-serial">
<summary><h3>🔗 esp32-usb-serial</h3></summary>
<table><tr><td>

**Project**: [esp32-usb-serial](https://github.com/luc-github/esp32-usb-serial)<br>
**Type**: Dependency<br>
**Version**: 🟢 v1.0.1<br>
**Description**: Arduino Library to use USB as OTG on ESP32 capable devices based on espressif IDF components<br>
**Language**: C++<br>
**Health Score**: <span style="color: #ff0000">22.6%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`main`)</h4></summary>

```
Last commit: 2025-12-17 (#f76066f)
Author: Luc
```

> 🎉 No open issues

</details>

</details>

<hr>

<details open id="esp32ssdp">
<summary><h3>🔗 ESP32SSDP</h3></summary>
<table><tr><td>

**Project**: [ESP32SSDP](https://github.com/luc-github/ESP32SSDP)<br>
**Type**: Dependency<br>
**Version**: 🟢 v2.0.4<br>
**Description**: Simple SSDP library for ESP32<br>
**Language**: C++<br>
**Health Score**: <span style="color: #ff0000">25.5%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`v2.x`)</h4></summary>

```
Last commit: 2025-12-17 (#0dbf33a)
Author: Luc
```

<table>
<tr><th>Status</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>#48: <a href="https://github.com/luc-github/ESP32SSDP/issues/48">Device name can not contain <</a></td><td><code>2025-05-26</code></td><td><code>2025-05-26</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#35: <a href="https://github.com/luc-github/ESP32SSDP/issues/35">[BUG]Miss Send notify : NTS: ssdp:byebye when stopping ssdp server</a></td><td><code>2023-05-16</code></td><td><code>2023-05-16</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>#9: <a href="https://github.com/luc-github/ESP32SSDP/issues/9">[FEATURE REQUEST] Respont to multiple device types or callback?</a></td><td><code>2020-02-05</code></td><td><code>2020-02-21</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

</details>

<hr>

<details open id="espluaengine">
<summary><h3>🔗 EspLuaEngine</h3></summary>
<table><tr><td>

**Project**: [EspLuaEngine](https://github.com/luc-github/EspLuaEngine)<br>
**Type**: Dependency<br>
**Version**: 🟢 v1.0.3<br>
**Description**: Add Lua engine to your firmware using ESP boards<br>
**Language**: C<br>
**Health Score**: <span style="color: #ff0000">19.5%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`main`)</h4></summary>

```
Last commit: 2025-12-17 (#e4c3f46)
Author: Luc
```

> 🎉 No open issues

</details>

</details>

<hr>

<details open id="plugin_oled_display">
<summary><h3>🔗 plugin_oled_display</h3></summary>
<table><tr><td>

**Project**: [plugin_oled_display](https://github.com/luc-github/plugin_oled_display)<br>
**Type**: Dependency<br>
**Version**: 🟢 v1.0.1<br>
**Description**: grblHAL plugin for oled display<br>
**Language**: Python<br>
**Health Score**: <span style="color: #ff0000">19.0%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`main`)</h4></summary>

```
Last commit: 2025-12-17 (#e6f37b2)
Author: Luc
```

> 🎉 No open issues

</details>

</details>

<hr>

<details open id="ssdp_idf">
<summary><h3>🔗 SSDP_IDF</h3></summary>
<table><tr><td>

**Project**: [SSDP_IDF](https://github.com/luc-github/SSDP_IDF)<br>
**Type**: Dependency<br>
**Version**: 🟢 v1.0.0<br>
**Description**: SSDP IDF component for ESP32<br>
**Language**: C<br>
**Health Score**: <span style="color: #ff0000">20.3%</span>

</td></tr></table>

<details>
<summary><h4>🚀 Production Branch (`main`)</h4></summary>

```
Last commit: 2025-12-17 (#c65c52c)
Author: Luc
```

<table>
<tr><th>Status</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>#1: <a href="https://github.com/luc-github/SSDP_IDF/issues/1">[BUG]Miss send notify : NTS: ssdp:byebye when stopping ssdp server #35</a></td><td><code>2023-05-16</code></td><td><code>2023-05-16</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

</details>

<hr>

## 📋 Global Issues

<details open>
<summary><h3>🔍 All Open Issues</h3></summary>

<details>
<summary><b>📁 ESP3D</b></summary>

<table>
<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#1116: <a href="https://github.com/luc-github/ESP3D/issues/1116">websocket connection error</a></td><td><code>2026-01-18</code></td><td><code>2026-01-19</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#243: <a href="https://github.com/luc-github/ESP3D/issues/243">[FEATURE REQUEST]🦄GCODE Streamer Host definition for 3.X</a></td><td><code>2018-07-14</code></td><td><code>2025-12-08</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#795: <a href="https://github.com/luc-github/ESP3D/issues/795">[TODO]☑Code refactoring plan</a></td><td><code>2022-07-28</code></td><td><code>2025-03-26</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#568: <a href="https://github.com/luc-github/ESP3D/issues/568">[FEATURE REQUEST]🦄USB Disk support using CH376S chip</a></td><td><code>2021-01-24</code></td><td><code>2024-10-28</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#575: <a href="https://github.com/luc-github/ESP3D/issues/575">⏸️[FEATURE REQUEST]🦄Use better serial protocol communication</a></td><td><code>2021-02-01</code></td><td><code>2024-03-06</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

**Health Score**: <span style="color: #ff0000">0.0%</span>

<details>
<summary>📊 Health Score Details</summary>

| Metric | Score | Status |
|--------|--------|--------|
| Documentation | 0.0% | 🔴 Needs Attention |
**Documentation Suggestions:**
- Add more detailed README
- Create documentation directory
- Add usage examples
| Maintenance | 0.0% | 🔴 Needs Attention |
**Maintenance Suggestions:**
- Increase commit frequency
- Address stale issues
- Set up automated testing
| Activity | 0.0% | 🔴 Needs Attention |
**Activity Suggestions:**
- Engage with community
- Regular status updates
- Promote the project
| Community | 0.0% | 🔴 Needs Attention |
**Community Suggestions:**
- Add contributing guidelines
- Add code of conduct
- Welcome new contributors

</details>

<details>
<summary><b>📁 ESP3DLib</b></summary>

<table>
<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>🔧 3.0</td><td>#87: <a href="https://github.com/luc-github/ESP3DLib/issues/87">[Compatibility issue]SDFat library  in ESP3D 3.0 conflict with latest Marlin SD implementation</a></td><td><code>2025-03-22</code></td><td><code>2025-03-22</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 3.0</td><td>#39: <a href="https://github.com/luc-github/ESP3DLib/issues/39">[FEATURE REQUEST]ESP3DLib 3.0</a></td><td><code>2022-02-01</code></td><td><code>2024-12-21</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

**Health Score**: <span style="color: #ff0000">0.0%</span>

<details>
<summary>📊 Health Score Details</summary>

| Metric | Score | Status |
|--------|--------|--------|
| Documentation | 0.0% | 🔴 Needs Attention |
**Documentation Suggestions:**
- Add more detailed README
- Create documentation directory
- Add usage examples
| Maintenance | 0.0% | 🔴 Needs Attention |
**Maintenance Suggestions:**
- Increase commit frequency
- Address stale issues
- Set up automated testing
| Activity | 0.0% | 🔴 Needs Attention |
**Activity Suggestions:**
- Engage with community
- Regular status updates
- Promote the project
| Community | 0.0% | 🔴 Needs Attention |
**Community Suggestions:**
- Add contributing guidelines
- Add code of conduct
- Welcome new contributors

</details>

<details>
<summary><b>📁 ESP3D-WEBUI</b></summary>

<table>
<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#438: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/438">Adding a custom logo</a></td><td><code>2025-12-28</code></td><td><code>2026-01-19</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#390: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/390">[FEATURE REQUEST]Port surfacing wizard as extension </a></td><td><code>2024-06-02</code></td><td><code>2026-01-14</code></td><td style="color: #000000">normal</td></tr>
<tr><td>🔄</td><td>🚀 3.0</td><td>#439: <a href="https://github.com/luc-github/ESP3D-WEBUI/pull/439">Bump qs and express</a></td><td><code>2025-12-30</code></td><td><code>2025-12-30</code></td><td style="color: #000000">normal</td></tr>
<tr><td>🔄</td><td>🚀 3.0</td><td>#418: <a href="https://github.com/luc-github/ESP3D-WEBUI/pull/418">Updated to 2.1.3c0 version</a></td><td><code>2025-09-20</code></td><td><code>2025-09-23</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#414: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/414">[FEATURE REQUEST]Add filament runout sensor status to WEB UI</a></td><td><code>2025-08-31</code></td><td><code>2025-09-01</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#411: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/411">[FEATURE REQUEST] Flexible panels customizations to optimize empty space</a></td><td><code>2025-03-30</code></td><td><code>2025-03-30</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#244: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/244">CNC process visualization functionality</a></td><td><code>2022-05-14</code></td><td><code>2024-11-25</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#122: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/122">[FEATURE REQUEST]PCB and Engraving Milling autoleveling</a></td><td><code>2020-10-10</code></td><td><code>2024-10-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#106: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/106">[FEATURE REQUEST] Bed Mesh Leveling Visualizer</a></td><td><code>2020-07-22</code></td><td><code>2024-10-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#265: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/265">[FEATURE REQUEST]Integrate the [ ESP700] command into the button</a></td><td><code>2022-09-18</code></td><td><code>2024-10-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#85: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/85">[FEATURE REQUEST]Be able to autodiscover all ESP3D devices and agregate them</a></td><td><code>2020-01-04</code></td><td><code>2022-08-15</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 3.0</td><td>#242: <a href="https://github.com/luc-github/ESP3D-WEBUI/issues/242">[FEATURE REQUEST]Configuration  Wizard </a></td><td><code>2022-05-10</code></td><td><code>2022-06-06</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

**Health Score**: <span style="color: #ff0000">0.0%</span>

<details>
<summary>📊 Health Score Details</summary>

| Metric | Score | Status |
|--------|--------|--------|
| Documentation | 0.0% | 🔴 Needs Attention |
**Documentation Suggestions:**
- Add more detailed README
- Create documentation directory
- Add usage examples
| Maintenance | 0.0% | 🔴 Needs Attention |
**Maintenance Suggestions:**
- Increase commit frequency
- Address stale issues
- Set up automated testing
| Activity | 0.0% | 🔴 Needs Attention |
**Activity Suggestions:**
- Engage with community
- Regular status updates
- Promote the project
| Community | 0.0% | 🔴 Needs Attention |
**Community Suggestions:**
- Add contributing guidelines
- Add code of conduct
- Welcome new contributors

</details>

<details>
<summary><b>📁 ESP3D-TFT</b></summary>

<table>
<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#82: <a href="https://github.com/luc-github/ESP3D-TFT/issues/82">[FEATURE REQUEST] Support for MKS DLC32 MAX LCD [ESP-TFT35 v4.1]</a></td><td><code>2025-12-28</code></td><td><code>2026-01-17</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#81: <a href="https://github.com/luc-github/ESP3D-TFT/issues/81">The serial port cannot be connected to the printer, but the USB serial port can</a></td><td><code>2025-05-19</code></td><td><code>2025-07-29</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#54: <a href="https://github.com/luc-github/ESP3D-TFT/issues/54">[FEATURE REQUEST]Move to lvgl 9.0</a></td><td><code>2024-01-17</code></td><td><code>2025-05-08</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#55: <a href="https://github.com/luc-github/ESP3D-TFT/issues/55">[FEATURE REQUEST]Code review / refactoring / improvement</a></td><td><code>2024-01-19</code></td><td><code>2024-12-14</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#76: <a href="https://github.com/luc-github/ESP3D-TFT/issues/76">[FEATURE REQUEST]Add Lua interpreter support like in ESP3D</a></td><td><code>2024-10-13</code></td><td><code>2024-10-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#74: <a href="https://github.com/luc-github/ESP3D-TFT/issues/74">[FEATURE REQUEST]Add BTT GCODE thumbnails</a></td><td><code>2024-08-14</code></td><td><code>2024-08-14</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#67: <a href="https://github.com/luc-github/ESP3D-TFT/issues/67">[FEATURE REQUEST]Add support of macro defined by webui on screen</a></td><td><code>2024-04-21</code></td><td><code>2024-08-13</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#53: <a href="https://github.com/luc-github/ESP3D-TFT/issues/53">[FEATURE REQUEST]Do better snapshot code with no memory need</a></td><td><code>2024-01-07</code></td><td><code>2024-01-07</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#12: <a href="https://github.com/luc-github/ESP3D-TFT/issues/12">[FEATURE REQUEST]WhatsApp Notification</a></td><td><code>2023-02-20</code></td><td><code>2023-02-20</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🔧 main</td><td>#5: <a href="https://github.com/luc-github/ESP3D-TFT/issues/5">[ENHANCEMENT]Add Pin interrupt support on FT5X06 when supported to save mcu time instead of doing permanent polling</a></td><td><code>2022-10-01</code></td><td><code>2022-10-01</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

**Health Score**: <span style="color: #ff0000">0.0%</span>

<details>
<summary>📊 Health Score Details</summary>

| Metric | Score | Status |
|--------|--------|--------|
| Documentation | 0.0% | 🔴 Needs Attention |
**Documentation Suggestions:**
- Add more detailed README
- Create documentation directory
- Add usage examples
| Maintenance | 0.0% | 🔴 Needs Attention |
**Maintenance Suggestions:**
- Increase commit frequency
- Address stale issues
- Set up automated testing
| Activity | 0.0% | 🔴 Needs Attention |
**Activity Suggestions:**
- Engage with community
- Regular status updates
- Promote the project
| Community | 0.0% | 🔴 Needs Attention |
**Community Suggestions:**
- Add contributing guidelines
- Add code of conduct
- Welcome new contributors

</details>

<details>
<summary><b>📁 ESP3D-Configurator</b></summary>

<table>
<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>🚀 main</td><td>#28: <a href="https://github.com/luc-github/ESP3D-Configurator/issues/28">[FEATURE REQUEST] Configure Client mode</a></td><td><code>2025-03-10</code></td><td><code>2025-03-10</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 main</td><td>#16: <a href="https://github.com/luc-github/ESP3D-Configurator/issues/16">[FEATURE REQUEST]Web Flasher Tool</a></td><td><code>2023-05-18</code></td><td><code>2023-05-18</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 main</td><td>#5: <a href="https://github.com/luc-github/ESP3D-Configurator/issues/5">[Information]Devt status</a></td><td><code>2022-06-18</code></td><td><code>2022-08-18</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

**Health Score**: <span style="color: #ff0000">0.0%</span>

<details>
<summary>📊 Health Score Details</summary>

| Metric | Score | Status |
|--------|--------|--------|
| Documentation | 0.0% | 🔴 Needs Attention |
**Documentation Suggestions:**
- Add more detailed README
- Create documentation directory
- Add usage examples
| Maintenance | 0.0% | 🔴 Needs Attention |
**Maintenance Suggestions:**
- Increase commit frequency
- Address stale issues
- Set up automated testing
| Activity | 0.0% | 🔴 Needs Attention |
**Activity Suggestions:**
- Engage with community
- Regular status updates
- Promote the project
| Community | 0.0% | 🔴 Needs Attention |
**Community Suggestions:**
- Add contributing guidelines
- Add code of conduct
- Welcome new contributors

</details>

<details>
<summary><b>📁 esp3d.io</b></summary>

<table>
<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>🚀 main</td><td>#49: <a href="https://github.com/luc-github/esp3d.io/issues/49">List external devices  tested / supported by ESP3D</a></td><td><code>2025-02-26</code></td><td><code>2025-02-26</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 main</td><td>#8: <a href="https://github.com/luc-github/esp3d.io/issues/8">Do a description page for each WebUI panel / Settings</a></td><td><code>2023-02-28</code></td><td><code>2023-02-28</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 main</td><td>#6: <a href="https://github.com/luc-github/esp3d.io/issues/6">Add Default setting description page</a></td><td><code>2023-02-28</code></td><td><code>2023-02-28</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

**Health Score**: <span style="color: #ff0000">0.0%</span>

<details>
<summary>📊 Health Score Details</summary>

| Metric | Score | Status |
|--------|--------|--------|
| Documentation | 0.0% | 🔴 Needs Attention |
**Documentation Suggestions:**
- Add more detailed README
- Create documentation directory
- Add usage examples
| Maintenance | 0.0% | 🔴 Needs Attention |
**Maintenance Suggestions:**
- Increase commit frequency
- Address stale issues
- Set up automated testing
| Activity | 0.0% | 🔴 Needs Attention |
**Activity Suggestions:**
- Engage with community
- Regular status updates
- Promote the project
| Community | 0.0% | 🔴 Needs Attention |
**Community Suggestions:**
- Add contributing guidelines
- Add code of conduct
- Welcome new contributors

</details>

<details>
<summary><b>📁 ESP32SSDP</b></summary>

<table>
<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>🚀 v2.x</td><td>#48: <a href="https://github.com/luc-github/ESP32SSDP/issues/48">Device name can not contain <</a></td><td><code>2025-05-26</code></td><td><code>2025-05-26</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 v2.x</td><td>#35: <a href="https://github.com/luc-github/ESP32SSDP/issues/35">[BUG]Miss Send notify : NTS: ssdp:byebye when stopping ssdp server</a></td><td><code>2023-05-16</code></td><td><code>2023-05-16</code></td><td style="color: #000000">normal</td></tr>
<tr><td>⭕</td><td>🚀 v2.x</td><td>#9: <a href="https://github.com/luc-github/ESP32SSDP/issues/9">[FEATURE REQUEST] Respont to multiple device types or callback?</a></td><td><code>2020-02-05</code></td><td><code>2020-02-21</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

**Health Score**: <span style="color: #ff0000">0.0%</span>

<details>
<summary>📊 Health Score Details</summary>

| Metric | Score | Status |
|--------|--------|--------|
| Documentation | 0.0% | 🔴 Needs Attention |
**Documentation Suggestions:**
- Add more detailed README
- Create documentation directory
- Add usage examples
| Maintenance | 0.0% | 🔴 Needs Attention |
**Maintenance Suggestions:**
- Increase commit frequency
- Address stale issues
- Set up automated testing
| Activity | 0.0% | 🔴 Needs Attention |
**Activity Suggestions:**
- Engage with community
- Regular status updates
- Promote the project
| Community | 0.0% | 🔴 Needs Attention |
**Community Suggestions:**
- Add contributing guidelines
- Add code of conduct
- Welcome new contributors

</details>

<details>
<summary><b>📁 SSDP_IDF</b></summary>

<table>
<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>
<tr><td>⭕</td><td>🚀 main</td><td>#1: <a href="https://github.com/luc-github/SSDP_IDF/issues/1">[BUG]Miss send notify : NTS: ssdp:byebye when stopping ssdp server #35</a></td><td><code>2023-05-16</code></td><td><code>2023-05-16</code></td><td style="color: #000000">normal</td></tr>
</table>

</details>

**Health Score**: <span style="color: #ff0000">0.0%</span>

<details>
<summary>📊 Health Score Details</summary>

| Metric | Score | Status |
|--------|--------|--------|
| Documentation | 0.0% | 🔴 Needs Attention |
**Documentation Suggestions:**
- Add more detailed README
- Create documentation directory
- Add usage examples
| Maintenance | 0.0% | 🔴 Needs Attention |
**Maintenance Suggestions:**
- Increase commit frequency
- Address stale issues
- Set up automated testing
| Activity | 0.0% | 🔴 Needs Attention |
**Activity Suggestions:**
- Engage with community
- Regular status updates
- Promote the project
| Community | 0.0% | 🔴 Needs Attention |
**Community Suggestions:**
- Add contributing guidelines
- Add code of conduct
- Welcome new contributors

</details>

</details>

## 📈 Recent Activity

<details>
<summary>Click to view recent activity</summary>

### Last 7 Days

| Activity | Count |
|----------|--------|
| Commits | 24 |
| New Issues | 4 |
| Closed Issues | 0 |
| Active Contributors | 3 |

### Activity Heatmap

```
    00 03 06 09 12 15 18 21
    -----------------------
Mon 🟨 🟨 🟩 🟨 🟩 🟦 🟦 🟩
Tue 🟦 🟩 🟨 🟨 🟩 🟦 🟦 🟦
Wed 🟩 🟨 🟨 🟨 🟩 🟦 🟦 🟩
Thu 🟩 🟥 🟥 🟨 🟦 🟦 ⬜ 🟦
Fri 🟩 🟨 🟩 🟩 🟩 🟦 🟦 🟦
Sat 🟦 🟩 🟨 🟩 🟩 🟦 ⬜ ⬜
Sun 🟨 🟩 🟨 🟩 🟩 🟦 🟦 🟦

Legend:
⬜ No activity 🟦 Low (1-2 commits) 🟩 Moderate (3-5 commits) 🟨 High (6-10 commits) 🟥 Very High (>10 commits)
```

</details>

<hr>

<div align="center">

*🔄 Last updated: 2026-01-19 01:23:04 UTC*

*Generated by [esp3d-portfolio](https://github.com/luc-github/esp3d-portfolio)*

</div>