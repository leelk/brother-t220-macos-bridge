// SPDX-License-Identifier: Apache-2.0
import AppKit

@main
final class SetupApp: NSObject, NSApplicationDelegate {
    private var window: NSWindow!
    static func main() {
        let app = NSApplication.shared
        let delegate = SetupApp()
        app.delegate = delegate
        app.setActivationPolicy(.regular)
        app.run()
    }
    func applicationDidFinishLaunching(_ notification: Notification) {
        window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 560, height: 320),
                          styleMask: [.titled, .closable, .miniaturizable], backing: .buffered, defer: false)
        window.title = "Brother T220 Native Setup — Experimental"
        window.center()
        let stack = NSStackView()
        stack.orientation = .vertical
        stack.alignment = .leading
        stack.spacing = 16
        stack.translatesAutoresizingMaskIntoConstraints = false
        let title = NSTextField(labelWithString: "Native printing for Brother DCP-T220")
        title.font = .boldSystemFont(ofSize: 20)
        stack.addArrangedSubview(title)
        let note = NSTextField(wrappingLabelWithString: "Experimental development build. Physical output and colour accuracy are not yet verified. Connect one DCP-T220 by USB, then add the native queue. Choose Brother_T220_Native in Cmd+P. No Docker or background app is required. Setup never prints a test automatically.")
        stack.addArrangedSubview(note)
        for (label, operation) in [("Add or Refresh Native Printer", "configure"), ("Restore Previous Native Queue", "rollback"), ("Remove Native Queue", "remove")] {
            let button = NSButton(title: label, target: self, action: #selector(performOperation(_:)))
            button.identifier = NSUserInterfaceItemIdentifier(operation)
            stack.addArrangedSubview(button)
        }
        let help = NSTextField(wrappingLabelWithString: "Removing the native queue keeps its files and leaves the Docker fallback unchanged. Close this app after setup; macOS handles printing on demand.")
        help.font = .systemFont(ofSize: 11)
        stack.addArrangedSubview(help)
        window.contentView!.addSubview(stack)
        NSLayoutConstraint.activate([
            stack.leadingAnchor.constraint(equalTo: window.contentView!.leadingAnchor, constant: 24),
            stack.trailingAnchor.constraint(equalTo: window.contentView!.trailingAnchor, constant: -24),
            stack.topAnchor.constraint(equalTo: window.contentView!.topAnchor, constant: 24)
        ])
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }
    @objc private func performOperation(_ sender: NSButton) {
        guard let operation = sender.identifier?.rawValue, ["configure", "rollback", "remove"].contains(operation) else { return }
        sender.isEnabled = false
        defer { sender.isEnabled = true }
        // All command text is fixed/allowlisted, never derived from printer URIs or document data.
        let command = "/Library/Printers/leelk/BrotherT220/manage-driver.sh " + operation
        let source = "do shell script \"" + command + "\" with administrator privileges"
        var error: NSDictionary?
        let result = NSAppleScript(source: source)?.executeAndReturnError(&error)
        let alert = NSAlert()
        if let error = error {
            alert.messageText = "Setup did not complete"
            alert.informativeText = error[NSAppleScript.errorMessage] as? String ?? "No system changes were confirmed."
        } else {
            alert.messageText = "Setup operation finished"
            alert.informativeText = result?.stringValue ?? "No test print was submitted."
        }
        alert.runModal()
    }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { true }
}
