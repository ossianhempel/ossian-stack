# Hosting And Integration

Read for requested hosting and app integration. Follow the scope and safety contract in the skill entry point.

## Hosting Guidance

### GitHub Pages (Free, Recommended for Indie Devs)

1. Create `docs/` folder in your repo
2. Add privacy-policy.md, terms-of-service.md, eula.md
3. Enable GitHub Pages in repo Settings > Pages > Source: `/docs`
4. Your URL: `https://yourusername.github.io/yourapp/privacy-policy`

### In-App Display

```swift
// Option 1: WKWebView for hosted HTML
import WebKit

struct LegalDocumentView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView { WKWebView() }
    func updateUIView(_ webView: WKWebView, context: Context) {
        webView.load(URLRequest(url: url))
    }
}

// Option 2: Bundled Markdown rendered as Text
struct PrivacyPolicyView: View {
    var body: some View {
        ScrollView {
            Text(LocalizedStringKey(privacyPolicyMarkdown))
                .padding()
                .textSelection(.enabled)
        }
        .navigationTitle("Privacy Policy")
    }
}
```

### Apple Requirements for Privacy Policy URL

- Must be publicly accessible (not behind login or in-app only)
- Must be a working URL at all times (Apple checks during review)
- Required in App Store Connect under "App Privacy"
- Must also be accessible from within the app (Settings or About screen)
