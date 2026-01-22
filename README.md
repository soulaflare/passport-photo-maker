# Passport Photo Maker

A free, privacy-focused passport photo maker that runs entirely in your browser. No uploads, no servers, no tracking.

**Live Demo:** [https://soulaflare.github.io/passport-photo-maker](https://soulaflare.github.io/passport-photo-maker)

**Repository:** [https://github.com/soulaflare/passport-photo-maker](https://github.com/soulaflare/passport-photo-maker)

---

## Features

- **100% Client-Side** — Your photos never leave your device
- **Multiple Formats** — International (ICAO), USA, and Canada sizes
- **Smart Guides** — Face and eye zone overlays based on official specifications
- **Drag to Position** — Intuitive drag-and-drop photo adjustment
- **Optimized Output** — 300 DPI with JPEG compression under 1 MB
- **Mobile Friendly** — Works on phones with camera capture support

---

## Supported Photo Formats

| Country | Dimensions | Pixels (300 DPI) | Face Height | Use Case |
|---------|------------|------------------|-------------|----------|
| **International (ICAO)** | 35 × 45 mm | 413 × 531 px | 32-36 mm | EU, UK, Australia, Schengen, most countries |
| **USA** | 2 × 2 inches | 600 × 600 px | 25-35 mm | US Passport & Visa |
| **Canada** | 50 × 70 mm | 591 × 827 px | 31-36 mm | Canadian Passport |

---

## How It Works

1. **Select your photo size** — Choose from International, USA, or Canada
2. **Upload a photo** — Click or drag-and-drop (supports camera on mobile)
3. **Adjust positioning** — Drag to reposition, use slider to zoom
4. **Align with guides** — Position eyes in the green zone, face within the oval
5. **Download** — Get a JPEG at 300 DPI, under 1 MB, with proper metadata

---

## Privacy

This tool processes everything locally in your browser using the HTML5 Canvas API.

- No server uploads
- No cookies or tracking
- No account required
- Works offline (after initial load)

---

## Technical Details

- **Single HTML file** — No build process, no dependencies
- **Canvas API** — For image manipulation and rendering
- **JFIF Patching** — Embeds 300 DPI metadata directly into JPEG binary
- **Binary Search Compression** — Finds optimal JPEG quality to stay under 1 MB
- **Responsive Design** — Mobile-first CSS with touch support

### Output Specifications

- Format: JPEG
- Resolution: 300 DPI
- Max file size: 1 MB
- Color space: sRGB

---

## Development

No build tools required. Just open `index.html` in a browser.

```bash
# Clone the repository
git clone https://github.com/soulaflare/passport-photo-maker.git

# Open in browser
open index.html
```

---

## Sources & Standards

Photo specifications based on:
- [ICAO Doc 9303](https://www.icao.int/publications/pages/publication.aspx?docnum=9303) — Machine Readable Travel Documents
- [US State Department](https://travel.state.gov/content/travel/en/passports/how-apply/photos.html) — US Passport Photo Requirements
- [Canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/services/canadian-passports/photos.html) — Canadian Passport Photo Specifications

---

## License

MIT License — Free for personal and commercial use.

---

## Contributing

Contributions welcome! Feel free to open issues or submit pull requests.

Potential improvements:
- Additional country formats
- Background removal
- Print layout (multiple photos per sheet)
- Face detection for auto-centering
