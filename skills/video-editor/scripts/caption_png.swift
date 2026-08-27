#!/usr/bin/env swift

import AppKit
import Foundation

func color(_ hex: String) -> NSColor {
    let cleaned = hex.trimmingCharacters(in: CharacterSet(charactersIn: "#"))
    guard cleaned.count == 6, let value = Int(cleaned, radix: 16) else { return .white }
    return NSColor(
        red: CGFloat((value >> 16) & 0xff) / 255,
        green: CGFloat((value >> 8) & 0xff) / 255,
        blue: CGFloat(value & 0xff) / 255,
        alpha: 1
    )
}

guard CommandLine.arguments.count == 13 else {
    fputs("usage: caption_png.swift output width height text font size primary highlight highlightColor outline outlineWidth\n", stderr)
    exit(2)
}

let args = CommandLine.arguments
let output = args[1]
let width = CGFloat(Double(args[2])!)
let height = CGFloat(Double(args[3])!)
let text = args[4]
let fontName = args[5]
let fontSize = CGFloat(Double(args[6])!)
let primary = color(args[7])
let highlight = args[8]
let highlightColor = color(args[9])
let outline = color(args[10])
let outlineWidth = CGFloat(Double(args[11])!)
let marginV = CGFloat(Double(args[12])!)

let image = NSImage(size: NSSize(width: width, height: height))
image.lockFocus()
NSColor.clear.setFill()
NSRect(x: 0, y: 0, width: width, height: height).fill()

let paragraph = NSMutableParagraphStyle()
paragraph.alignment = .center
paragraph.lineBreakMode = .byWordWrapping
let font = NSFont(name: fontName, size: fontSize) ?? NSFont.boldSystemFont(ofSize: fontSize)
let attributed = NSMutableAttributedString(string: text, attributes: [
    .font: font,
    .foregroundColor: primary,
    .strokeColor: outline,
    .strokeWidth: -outlineWidth,
    .paragraphStyle: paragraph,
])
if !highlight.isEmpty, let range = text.lowercased().range(of: highlight.lowercased()) {
    attributed.addAttribute(.foregroundColor, value: highlightColor, range: NSRange(range, in: text))
}
let rect = NSRect(x: width * 0.08, y: marginV, width: width * 0.84, height: min(height * 0.34, fontSize * 4.5))
attributed.draw(with: rect, options: [.usesLineFragmentOrigin, .usesFontLeading])
image.unlockFocus()

guard let tiff = image.tiffRepresentation,
      let bitmap = NSBitmapImageRep(data: tiff),
      let png = bitmap.representation(using: .png, properties: [:]) else {
    fputs("failed to encode caption PNG\n", stderr)
    exit(1)
}
try png.write(to: URL(fileURLWithPath: output))
