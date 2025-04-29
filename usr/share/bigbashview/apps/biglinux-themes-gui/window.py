"""
Main window module for BigLinux Themes GUI.
Implements the main application window and UI functionality.
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

# Import the translation function
from i18n import _
from theme_manager import ThemeManager
from desktop_manager import DesktopManager


class ThemesWindow(Adw.ApplicationWindow):
    """Main application window for BigLinux Themes."""

    def __init__(self, **kwargs):
        """Initialize the main window."""
        super().__init__(
            title=_("BigLinux Themes"), default_width=1000, default_height=620, **kwargs
        )

        self.theme_manager = ThemeManager()
        self.desktop_manager = DesktopManager()

        self.selected_theme = None
        self.selected_desktop = None

        # Setup UI elements
        self._setup_css()
        self._setup_ui()
        self._load_themes_and_desktops()

    def _setup_css(self):
        """Set up custom CSS styling."""
        css_provider = Gtk.CssProvider()
        css = """
            /* Base style for interactive items */
            .clickable-item {
            transition: 500ms ease;
            border-radius: 10px;
            }
            
            /* Match keyboard navigation style with outline instead of border */
            flowboxchild:hover {
            outline: 2px solid alpha(@theme_selected_bg_color, 0.5);
            outline-offset: -2px;
            border-radius: 10px;
            }

            .active-bg { background-color: alpha(var(--accent-bg-color), 0.05); }
            
            /* Desktop section background */
            .desktop-section {
            background-color: var(--view-bg-color);
            }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _setup_ui(self):
        """Set up the user interface."""
        # Use toast overlay as main container to show notifications
        self.toast_overlay = Adw.ToastOverlay()
        self.set_content(self.toast_overlay)

        # Create modern split view for themes and desktops with integrated headers
        self.split_view = Adw.OverlaySplitView()

        # Set the split view directly as the child of the toast overlay
        self.toast_overlay.set_child(self.split_view)

        # Create sidebar content with header
        theme_toolbar_view = Adw.ToolbarView()

        # Create theme header with automatic decoration handling
        theme_header = Adw.HeaderBar()
        # Use Adw.WindowTitle for proper styling
        theme_title = Adw.WindowTitle(title=_("Themes"), subtitle="")
        theme_header.set_title_widget(theme_title)
        theme_toolbar_view.add_top_bar(theme_header)

        # Theme content area
        theme_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        theme_box.set_margin_start(12)
        theme_box.set_margin_end(12)
        theme_box.set_margin_top(0)
        theme_box.set_margin_bottom(6)

        theme_scroll = Gtk.ScrolledWindow()
        theme_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        theme_scroll.set_vexpand(True)
        theme_box.append(theme_scroll)

        self.theme_flowbox = Gtk.FlowBox()
        self.theme_flowbox.set_valign(Gtk.Align.START)
        self.theme_flowbox.set_max_children_per_line(1)
        # Start with NONE selection mode to prevent auto-selection
        self.theme_flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.theme_flowbox.connect("child-activated", self._on_theme_selected)
        theme_scroll.set_child(self.theme_flowbox)

        theme_toolbar_view.set_content(theme_box)
        self.split_view.set_sidebar(theme_toolbar_view)

        # Right side: Desktops (Content) with header
        desktop_toolbar_view = Adw.ToolbarView()
        desktop_toolbar_view.add_css_class("desktop-section")

        # Create desktop header with automatic decoration handling
        desktop_header = Adw.HeaderBar()
        # Use Adw.WindowTitle for proper styling
        desktop_title = Adw.WindowTitle(title=_("Desktop"), subtitle="")
        desktop_header.set_title_widget(desktop_title)
        desktop_toolbar_view.add_top_bar(desktop_header)

        # Desktop content area
        desktop_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        desktop_box.set_margin_start(12)
        desktop_box.set_margin_end(12)
        desktop_box.set_margin_top(0)
        desktop_box.set_margin_bottom(6)
        desktop_box.set_vexpand(True)
        desktop_box.set_hexpand(True)

        desktop_scroll = Gtk.ScrolledWindow()
        desktop_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        desktop_scroll.set_vexpand(True)  # Allow vertical expansion
        desktop_box.append(desktop_scroll)

        self.desktop_flowbox = Gtk.FlowBox()
        self.desktop_flowbox.set_valign(Gtk.Align.START)
        # Start with NO selection mode to prevent auto-selection
        self.desktop_flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        # Align fill might conflict with valign start, let's stick to START for vertical alignment

        # Allow children to have different sizes
        self.desktop_flowbox.set_homogeneous(False)  # Changed from True
        self.desktop_flowbox.set_row_spacing(12)
        self.desktop_flowbox.set_column_spacing(12)

        # Make the layout adaptive to screen size
        self.desktop_flowbox.set_min_children_per_line(2)  # At least 1 column
        self.desktop_flowbox.set_max_children_per_line(3)  # At most 3 columns

        # Use resize notification for adaptive layout
        self.desktop_flowbox.connect("child-activated", self._on_desktop_selected)
        desktop_scroll.set_child(self.desktop_flowbox)

        # Set the content in the toolbar view
        desktop_toolbar_view.set_content(desktop_box)

        # Set desktop content area to split view
        self.split_view.set_content(desktop_toolbar_view)

    def _load_themes_and_desktops(self):
        """Load available themes and desktop configurations."""
        # Load themes
        current_theme = self.theme_manager.get_current_theme()
        theme_list = self.theme_manager.get_theme_list()

        for theme_name in theme_list:
            theme_widget = self.theme_manager.create_theme_widget(theme_name)
            theme_widget.set_margin_top(3)
            theme_widget.set_margin_bottom(3)

            flowbox_child = Gtk.FlowBoxChild()
            flowbox_child.set_child(theme_widget)
            flowbox_child.set_margin_top(0)
            flowbox_child.set_margin_bottom(0)

            # Add custom property to identify the theme
            flowbox_child.set_name(theme_name)
            #  margin top 0
            flowbox_child.set_margin_top(0)
            flowbox_child.set_margin_bottom(0)

            # Highlight current theme with a checkmark
            if theme_name == current_theme:
                flowbox_child.add_css_class("frame")
                flowbox_child.add_css_class("accent")
                flowbox_child.add_css_class("active-bg")
                check_icon = Gtk.Image.new_from_icon_name("object-select-symbolic")
                check_icon.add_css_class("success")
                check_icon.set_margin_top(10)
                check_icon.set_margin_end(10)
                check_icon.set_halign(Gtk.Align.END)
                check_icon.set_valign(Gtk.Align.START)

                # Get the theme widget and add the checkmark using an overlay container
                theme_widget = flowbox_child.get_child()

                if isinstance(theme_widget, Gtk.Box):
                    # Create an overlay container
                    overlay = Gtk.Overlay()

                    # Remove the widget from the flowbox child first
                    flowbox_child.set_child(None)

                    # Add the theme widget to the overlay as the main content
                    overlay.set_child(theme_widget)

                    # Add the check icon as an overlay
                    overlay.add_overlay(check_icon)

                    # Set the overlay as the child of the flowbox child
                    flowbox_child.set_child(overlay)

            self.theme_flowbox.append(flowbox_child)

        # Load desktop configurations
        current_desktop = self.desktop_manager.get_current_desktop()
        desktop_list = self.desktop_manager.get_desktop_list()

        for desktop_name in desktop_list:
            desktop_widget = self.desktop_manager.create_desktop_widget(desktop_name)
            flowbox_child = Gtk.FlowBoxChild()
            flowbox_child.set_halign(Gtk.Align.CENTER)
            flowbox_child.set_valign(Gtk.Align.FILL)
            flowbox_child.set_child(desktop_widget)

            # Add custom property to identify the desktop
            flowbox_child.set_name(desktop_name)

            # Highlight current desktop
            if desktop_name == current_desktop:
                flowbox_child.add_css_class("frame")
                flowbox_child.add_css_class("accent")
                flowbox_child.add_css_class("active-bg")

                # Create a checkmark icon for the current desktop
                check_icon = Gtk.Image.new_from_icon_name("object-select-symbolic")
                check_icon.add_css_class("success")
                check_icon.set_halign(Gtk.Align.END)
                check_icon.set_valign(Gtk.Align.START)
                check_icon.set_margin_top(20)
                check_icon.set_margin_end(20)

                # Get the desktop widget and add the checkmark using an overlay
                desktop_widget = flowbox_child.get_child()
                if isinstance(desktop_widget, Gtk.Box):
                    # Create an overlay container
                    overlay = Gtk.Overlay()

                    # Remove the widget from the flowbox child first
                    flowbox_child.set_child(None)

                    # Add the desktop widget to the overlay as the main content
                    overlay.set_child(desktop_widget)

                    # Add the check icon as an overlay
                    overlay.add_overlay(check_icon)

                    # Set the overlay as the child of the flowbox child
                    flowbox_child.set_child(overlay)

            self.desktop_flowbox.append(flowbox_child)

    def _on_theme_selected(self, flowbox, child):
        """Handle theme selection in the FlowBox."""
        theme_name = child.get_name()
        self.selected_theme = theme_name

        # Explicitly refresh current theme to ensure we have the latest value
        current_theme = self.theme_manager.get_current_theme()
        print(f"Selected theme: {theme_name}, Current theme: {current_theme}")

        # Check if same theme is selected
        if theme_name.strip() == current_theme.strip():
            print("Showing theme confirmation dialog for reapplication")
            # Create and show confirmation dialog for reapplying the same theme
            dialog = Adw.MessageDialog(
                transient_for=self,
                heading=_("Confirm Theme Change"),
                body=_("Do you want to apply the selected theme again?"),
            )
            dialog.add_response("cancel", _("Cancel"))
            dialog.add_response("apply", _("Apply"))
            dialog.set_default_response("cancel")
            dialog.set_response_appearance("apply", Adw.ResponseAppearance.SUGGESTED)
            dialog.connect("response", self._on_theme_confirm_response)
            dialog.present()
        else:
            print("Showing theme confirmation dialog for new theme")
            # Create and show confirmation dialog for applying a different theme
            dialog = Adw.MessageDialog(
                transient_for=self,
                heading=_("Confirm Theme Change"),
                body=_("Do you want to change the theme to {}?").format(
                    theme_name.replace("-", " ")
                ),
            )
            dialog.add_response("cancel", _("Cancel"))
            dialog.add_response("apply", _("Apply"))
            dialog.set_default_response("cancel")
            dialog.set_response_appearance("apply", Adw.ResponseAppearance.SUGGESTED)
            dialog.connect("response", self._on_theme_confirm_response)
            dialog.present()

    def _on_desktop_selected(self, flowbox, child):
        """Handle desktop selection in the FlowBox."""
        desktop_name = child.get_name()
        self.selected_desktop = desktop_name
        current_desktop = self.desktop_manager.get_current_desktop()

        print(f"Selected desktop: {desktop_name}, Current desktop: {current_desktop}")

        if desktop_name == current_desktop:
            print("Showing desktop confirmation dialog")
            # Create and show confirmation dialog for reapplying the same desktop
            dialog = Adw.MessageDialog(
                transient_for=self,
                heading=_("Confirm Desktop Change"),
                body=_("Do you want to reapply a clean configuration of that desktop?"),
            )
            dialog.add_response("cancel", _("Cancel"))
            dialog.add_response("apply", _("Apply"))
            dialog.set_default_response("cancel")
            dialog.set_response_appearance("apply", Adw.ResponseAppearance.SUGGESTED)
            dialog.connect("response", self._on_desktop_confirm_response)
            dialog.present()
        else:
            # Check if desktop has been used before
            is_used = self.desktop_manager.is_desktop_used(desktop_name)
            print(f"Desktop used before: {is_used}")

            if is_used:
                print("Showing desktop restore dialog")
                # Create and show dialog for restore/clean choice
                dialog = Adw.MessageDialog(
                    transient_for=self,
                    heading=_("Configuration"),
                    body=_(
                        "You've used this desktop before, do you want to restore your customization or use the original configuration?"
                    ),
                )
                dialog.add_response("cancel", _("Cancel"))
                dialog.add_response("clean", _("Original"))
                dialog.add_response("restore", _("Restore"))
                dialog.set_default_response("cancel")
                dialog.set_response_appearance(
                    "clean", Adw.ResponseAppearance.SUGGESTED
                )
                dialog.set_response_appearance(
                    "restore", Adw.ResponseAppearance.SUGGESTED
                )
                dialog.connect("response", self._on_desktop_restore_response)
                dialog.present()
            else:
                print("Applying new desktop directly")
                # Apply new desktop with default configuration
                self._apply_desktop(desktop_name)

    def _on_theme_confirm_response(self, dialog, response):
        """Handle response from theme confirmation dialog."""
        print(f"Theme confirm dialog response: {response}")
        # Always dismiss the dialog first
        dialog.set_visible(False)

        # Then handle the response
        if response == "apply":
            print("Reapplying the same theme")
            self._apply_theme(self.selected_theme)
        elif response == "cancel":
            print("Theme reapplication cancelled")

    def _on_desktop_confirm_response(self, dialog, response):
        """Handle response from desktop confirmation dialog."""
        print(f"Desktop confirm dialog response: {response}")
        # Always dismiss the dialog first
        dialog.set_visible(False)

        # Then handle the response
        if response == "apply":
            print("Reapplying the desktop with clean option")
            self._apply_desktop(self.selected_desktop, "clean")
        elif response == "cancel":
            print("Desktop reapplication cancelled")

    def _on_desktop_restore_response(self, dialog, response):
        """Handle response from desktop restore/clean dialog."""
        print(f"Desktop restore dialog response: {response}")
        # Always dismiss the dialog first
        dialog.set_visible(False)

        # Then handle the response
        if response == "clean":
            print("Applying desktop with clean option")
            self._apply_desktop(self.selected_desktop, "clean")
        elif response == "restore":
            print("Applying desktop with restore option")
            self._apply_desktop(self.selected_desktop)
        elif response == "cancel":
            print("Desktop restore operation cancelled")

    def _add_checkmark_to_widget(self, flowbox_child):
        """Add a checkmark icon to a flowbox child item."""
        # Create a checkmark icon
        check_icon = Gtk.Image.new_from_icon_name("object-select-symbolic")
        check_icon.add_css_class("success")
        check_icon.set_halign(Gtk.Align.END)
        check_icon.set_valign(Gtk.Align.START)
        check_icon.set_margin_top(10)
        check_icon.set_margin_end(10)

        # Get the widget and add the checkmark using an overlay
        widget = flowbox_child.get_child()
        if isinstance(widget, Gtk.Box):
            # Create an overlay container
            overlay = Gtk.Overlay()

            # Remove the widget from the flowbox child first
            flowbox_child.set_child(None)

            # Add the widget to the overlay as the main content
            overlay.set_child(widget)

            # Add the check icon as an overlay
            overlay.add_overlay(check_icon)

            # Set the overlay as the child of the flowbox child
            flowbox_child.set_child(overlay)
        elif isinstance(widget, Gtk.Overlay):
            # The item already has an overlay, we just need to add another check icon
            widget.add_overlay(check_icon)

    def _apply_theme(self, theme_name):
        """Apply a theme and show notification."""
        try:
            print(f"Applying theme: {theme_name}")
            self.theme_manager.set_theme(theme_name)
            print("Theme application successful")

            # Update selected theme in UI
            i = 0
            child = self.theme_flowbox.get_child_at_index(i)
            updated_items = 0

            while child:
                if child.get_name() == theme_name:
                    # Add visual indicators
                    child.add_css_class("accent")
                    child.add_css_class("active-bg")
                    child.add_css_class("frame")
                    child.set_halign(Gtk.Align.END)
                    child.set_valign(Gtk.Align.START)

                    # Add checkmark to the selected item
                    self._add_checkmark_to_widget(child)

                    updated_items += 1
                else:
                    # Remove visual indicators
                    child.remove_css_class("accent")
                    child.remove_css_class("active-bg")
                    child.remove_css_class("frame")
                    child.set_halign(Gtk.Align.END)
                    child.set_valign(Gtk.Align.START)

                    # Remove any existing checkmark by recreating the child's content
                    widget = child.get_child()
                    if isinstance(widget, Gtk.Overlay):
                        # Extract the original content box from the overlay
                        content = widget.get_child()
                        if content:
                            # Remove from overlay and set directly as child
                            widget.set_child(None)
                            child.set_child(content)

                i += 1
                child = self.theme_flowbox.get_child_at_index(i)

            # Show toast notification
            self._show_change_toast()
        except Exception as e:
            print(f"ERROR applying theme: {e}")
            # Show error toast notification
            self._show_error_toast(f"Error applying theme: {str(e)}")

    def _apply_desktop(self, desktop_name, clean=""):
        """Apply a desktop configuration and show notification."""
        try:
            print(f"Applying desktop: {desktop_name}, clean option: '{clean}'")
            self.desktop_manager.set_desktop(desktop_name, clean)
            print("Desktop application successful")

            # Update selected desktop in UI
            i = 0
            child = self.desktop_flowbox.get_child_at_index(i)
            updated_items = 0

            while child:
                if child.get_name() == desktop_name:
                    # Add visual indicators
                    child.add_css_class("accent")
                    child.add_css_class("active-bg")
                    child.set_halign(Gtk.Align.CENTER)
                    child.set_valign(Gtk.Align.FILL)
                    child.add_css_class("frame")

                    # Add checkmark to the selected item
                    self._add_checkmark_to_widget(child)

                    print(f"Highlighted desktop: {child.get_name()}")
                    updated_items += 1
                else:
                    # Remove visual indicators
                    child.remove_css_class("accent")
                    child.remove_css_class("active-bg")
                    child.set_halign(Gtk.Align.CENTER)
                    child.set_valign(Gtk.Align.FILL)
                    child.remove_css_class("frame")

                    # Remove any existing checkmark by recreating the child's content
                    widget = child.get_child()
                    if isinstance(widget, Gtk.Overlay):
                        # Extract the original content box from the overlay
                        content = widget.get_child()
                        if content:
                            # Remove from overlay and set directly as child
                            widget.set_child(None)
                            child.set_child(content)

                i += 1
                child = self.desktop_flowbox.get_child_at_index(i)

            print(f"Updated {updated_items} desktop items in UI")

            # Show toast notification
            self._show_change_toast()
        except Exception as e:
            print(f"ERROR applying desktop: {e}")
            # Show error toast notification
            self._show_error_toast(f"Error applying desktop: {str(e)}")

    def _show_change_toast(self):
        """Show toast notification for theme/desktop changes."""
        toast = Adw.Toast.new(
            _(
                "The settings have been changed. To apply them throughout the system, log off and log in again."
            )
        )
        toast.set_timeout(5)
        self.toast_overlay.add_toast(toast)

    def _show_error_toast(self, message):
        """Show error toast notification."""
        toast = Adw.Toast.new(_(message))
        toast.set_timeout(5)
        toast.add_css_class("error")
        self.toast_overlay.add_toast(toast)
