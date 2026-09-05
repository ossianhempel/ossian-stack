# Element Rendering

Read for isolated transparent elements, cards, or widgets. Follow the scope and safety contract in the skill entry point.

## Element Rendering

Elements are rendered via `ImageRenderer` at 3x scale with transparency outside rounded corners.

### Cards / list rows

```swift
@MainActor
static func renderCards(items: [Item], theme: AppTheme) {
    let cardWidth: CGFloat = 380

    for item in items {
        let card = ItemCard(item: item, theme: theme)
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
            .frame(width: cardWidth)
            .background(theme.background)
            .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous))

        let renderer = ImageRenderer(content: card)
        renderer.scale = 3
        renderer.isOpaque = false
        renderer.proposedSize = .init(width: cardWidth, height: nil)

        guard let image = renderer.uiImage else { continue }
        MarketingCapture.writePNG(image, name: "card-\(slugify(item.name))", subfolder: "elements")
    }
}
```

### Widgets

Widget views require special handling because they normally run inside WidgetKit's process and rely on system-provided padding and backgrounds.

```swift
@MainActor
static func renderWidget(
    name: String,
    size: CGSize,
    cornerRadius: CGFloat? = nil,
    @ViewBuilder content: () -> some View
) {
    let isAccessory = size.height <= 80
    let radius = cornerRadius ?? (isAccessory ? 8 : 22)
    let contentPadding: CGFloat = isAccessory ? 0 : 16

    let view = content()
        .padding(contentPadding)
        .frame(width: size.width, height: size.height)
        .background(theme.background)
        .clipShape(RoundedRectangle(cornerRadius: radius, style: .continuous))
        .environment(\.colorScheme, .light)

    let renderer = ImageRenderer(content: view)
    renderer.scale = 3
    renderer.isOpaque = false
    renderer.proposedSize = .init(width: size.width, height: size.height)

    guard let image = renderer.uiImage else { return }
    MarketingCapture.writePNG(image, name: name, subfolder: "elements")
}

// Standard iPhone widget sizes (points, iPhone 14-17 size class)
enum WidgetSize {
    static let small  = CGSize(width: 170, height: 170)
    static let medium = CGSize(width: 364, height: 170)
    static let large  = CGSize(width: 364, height: 382)
    static let accessoryCircular    = CGSize(width: 76, height: 76)
    static let accessoryRectangular = CGSize(width: 172, height: 76)
    static let accessoryInline      = CGSize(width: 257, height: 26)
}

// Usage:
renderWidget(name: "widget-pulse-small", size: WidgetSize.small) {
    PulseSmallView(entry: PulseEntry(
        date: Date(),
        count: 2,
        streak: 5,
        lastItemName: "Morning Routine"
    ))
}
```

### Charts / standalone views

Any SwiftUI view can be rendered as an element. Wrap it the same way — explicit size, background, corner clip:

```swift
@MainActor
static func renderChart() {
    let chart = MyChartView(values: ChartData.sample)
        .frame(width: 420, height: 420)
        .background(theme.background)
        .clipShape(RoundedRectangle(cornerRadius: 32, style: .continuous))

    let renderer = ImageRenderer(content: chart)
    renderer.scale = 3
    renderer.isOpaque = false
    renderer.proposedSize = .init(width: 420, height: 420)

    guard let image = renderer.uiImage else { return }
    MarketingCapture.writePNG(image, name: "chart-overview", subfolder: "elements")
}
```
