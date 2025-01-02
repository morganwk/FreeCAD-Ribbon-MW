# *************************************************************************
# *                                                                       *
# * Copyright (c) 2019-2024 Hakan Seven, Geolta, Paul Ebbers              *
# *                                                                       *
# * This program is free software; you can redistribute it and/or modify  *
# * it under the terms of the GNU Lesser General Public License (LGPL)    *
# * as published by the Free Software Foundation; either version 3 of     *
# * the License, or (at your option) any later version.                   *
# * for detail see the LICENCE text file.                                 *
# *                                                                       *
# * This program is distributed in the hope that it will be useful,       *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# * GNU Library General Public License for more details.                  *
# *                                                                       *
# * You should have received a copy of the GNU Library General Public     *
# * License along with this program; if not, write to the Free Software   *
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# * USA                                                                   *
# *                                                                       *
# *************************************************************************
import FreeCAD as App
import FreeCADGui as Gui
from pathlib import Path
import textwrap

from PySide.QtGui import (
    QIcon,
    QAction,
    QFontMetrics,
    QFont,
    QTextOption,
    QCursor,
    QPalette,
    QEnterEvent,
)
from PySide.QtWidgets import (
    QToolButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMenu,
    QSpacerItem,
    QSizePolicy,
    QTextEdit,
    QStyleOption,
    QFrame,
    QGraphicsEffect,
)
from PySide.QtCore import Qt, QSize, QRect, QMargins, QEvent

import os
import sys
import Parameters_Ribbon
import Standard_Functions_RIbbon as StandardFunctions
import StyleMapping

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathScripts = os.path.join(os.path.dirname(__file__), "Scripts")
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)

translate = App.Qt.translate


class CustomControls:
    def LargeCustomToolButton(
        Text: str,
        Action: QAction,
        Icon: QIcon,
        IconSize: QSize,
        ButtonSize: QSize,
        FontSize: int = 10,
        showText=True,
        TextAlignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter,
        setWordWrap=True,
        MaxNumberOfLines=2,
        Menu: QMenu = None,
        MenuButtonSpace=10,
    ):
        # Define the controls
        btn = QToolButton()
        CommandButton = QToolButton()
        ArrowButton = QToolButton()
        Layout = QVBoxLayout()
        Label_Text = QTextEdit()
        # Define the parameters
        TextHeight = 0
        TextWidth = 0
        Space = 6
        if showText is False:
            Space = 0
        # Remove any trailing spaces
        Text = Text.strip()
        # Set the buttonSize
        CommandButton.setMaximumSize(ButtonSize)
        # Set the icon and its size
        CommandButton.setIcon(Icon)
        CommandButton.setIconSize(IconSize.expandedTo(CommandButton.size()))
        # Set the content margins to zero
        CommandButton.setContentsMargins(0, 0, 0, 0)
        # Add a actions if there is only one
        if len(Menu.actions()) == 0:
            CommandButton.addAction(Action)
        CommandButton.setDefaultAction(Action)

        # Define a vertical layout
        Layout = QVBoxLayout()
        # Add the command button
        Layout.addWidget(CommandButton)
        Layout.setAlignment(TextAlignment)
        # Set the content margins to zero
        Layout.setContentsMargins(0, 0, 0, 0)

        # if showText is False:
        if MenuButtonSpace < 12:
            MenuButtonSpace = 12

        # If text must not be show, set the text to an empty string
        # Still create a label to set up the button properly
        if showText is True and Text != "":
            # Create a label with the correct properties
            # Label_Text = QTextEdit()
            Label_Text.setReadOnly(True)
            Label_Text.setFrameShape(QFrame.Shape.NoFrame)
            Label_Text.setFrameShadow(QFrame.Shadow.Plain)
            Label_Text.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            Label_Text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            Label_Text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            Label_Text.document().setDocumentMargin(0)
            Label_Text.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            Label_Text.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # Set the font
            Font = QFont()
            Font.setPointSize(FontSize)
            Label_Text.setFont(Font)
            # If there is no WordWrap, set the ElideMode and the max number of lines to 1.
            if setWordWrap is False:
                # Determine the maximum length per line
                FontMetrics = QFontMetrics(Text)
                maxWidth = 0
                maxLength = 0
                for c in Text:
                    maxWidth = maxWidth + FontMetrics.boundingRectChar(c).width()
                    if maxWidth < ButtonSize.width():
                        maxLength = maxLength + 1
                    if maxWidth >= ButtonSize.width():
                        break
                # Set the text with a placeholder
                Text = textwrap.shorten(text=Text, width=maxLength, placeholder="...")
                Label_Text.setWordWrapMode(QTextOption.WrapMode.NoWrap)
                Label_Text.setText(Text)
                # Set the maximum number of lines to 1
                MaxNumberOfLines = 1
                # Set the proper alignment
                Label_Text.setAlignment(TextAlignment)
            # Determine the height of a single row
            SingleHeight = QFontMetrics(Font).boundingRect(Text).height() + 3
            # make sure that the label height is at least for two lines
            Label_Text.setMinimumHeight((SingleHeight * 1))
            Label_Text.setMaximumHeight((SingleHeight * MaxNumberOfLines) + 3)
            TextHeight = Label_Text.maximumHeight()
            # Set the width of the label based on the size of the button
            Label_Text.setFixedWidth(ButtonSize.width() + Space)
            # Adjust the size to be able to store the actual height
            Label_Text.adjustSize()
            # Set the textheight
            if setWordWrap is True:
                # Set the wrap mode
                Label_Text.setWordWrapMode(QTextOption.WrapMode.WordWrap)
                # Determine the maximum length per line
                FontMetrics = QFontMetrics(Text)
                maxWidth = 0
                maxLength = 0
                for c in Text:
                    maxWidth = maxWidth + FontMetrics.boundingRectChar(c).width()
                    if maxWidth < ButtonSize.width():
                        maxLength = maxLength + 1
                    if maxWidth >= ButtonSize.width():
                        break
                # Set the text, use the wrapper function. It will only return the set number of lines
                Label_Text.setText(StandardFunctions.ReturnWrappedText(Text, maxWidth, MaxNumberOfLines, False))
                # Adjust the size of the label
                Label_Text.setMaximumHeight((SingleHeight * MaxNumberOfLines) - 3)
                Label_Text.setAlignment(TextAlignment)
                Label_Text.adjustSize()
                # Update the parameters for later
                TextHeight = Label_Text.height()
                TextWidth = Label_Text.width()
            # Add the label with alignment
            Layout.addWidget(Label_Text)

        if Menu is not None and len(Menu.actions()) > 1:
            # Define a menu
            ArrowButton.setMenu(Menu)
            ArrowButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            # Set the height according the space for the menubutton
            ArrowButton.setFixedHeight(MenuButtonSpace)
            # Set the width according the commandbutton
            ArrowButton.setFixedWidth(CommandButton.width() + Space)
            ArrowButton.adjustSize()
            # Set the arrow to none
            ArrowButton.setArrowType(Qt.ArrowType.NoArrow)
            # Set the content margins
            ArrowButton.setContentsMargins(0, 0, 0, 0)
            # Add the Arrow button to the layout
            Layout.addWidget(ArrowButton)

            # Add the label to the area where the user can invoke the menu
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    ArrowButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom(event):
                    BorderColor = StyleMapping.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-top: 0px solid"
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 0px;border-bottom-right-radius: 2px"
                        + ";}"
                        + """QToolButton::menu-indicator {
                                subcontrol-origin: padding;
                                subcontrol-position: center top;
                            }"""
                    )
                    StyleSheet_Addition_Label = (
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-bottom: 0px solid"
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 0px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 0px"
                        + ";}"
                    )
                    if ArrowButton.underMouse():
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)
                    if Label_Text.underMouse():
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                ArrowButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

                # restore the stylesheets on leaving
                def leaveEventCustom(event):
                    StyleSheet = StyleMapping.ReturnStyleSheet(
                        control="toolbutton",
                        radius="2px",
                    )
                    StyleSheet_Addition = """QToolButton::menu-indicator {
                        subcontrol-origin: padding;
                        subcontrol-position: center top;
                    }"""
                    Label_Text.setStyleSheet(StyleSheet)
                    ArrowButton.setStyleSheet(StyleSheet_Addition + StyleSheet)

                Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
                ArrowButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
        else:
            MenuButtonSpace = 0
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    CommandButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom(event):
                    BorderColor = StyleMapping.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Label = (
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-top: 0px solid"
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 0px;border-bottom-right-radius: 2px"
                        + ";}"
                    )
                    StyleSheet_Addition_Command = (
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-bottom: 0px solid"
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 0px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 0px"
                        + ";}"
                    )
                    if CommandButton.underMouse():
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)
                    if Label_Text.underMouse():
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                CommandButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

                # restore the stylesheets on leaving
                def leaveEventCustom(event):
                    StyleSheet = StyleMapping.ReturnStyleSheet(
                        control="toolbutton",
                        radius="2px",
                    )
                    Label_Text.setStyleSheet(StyleSheet)
                    CommandButton.setStyleSheet(StyleSheet)

                Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
                CommandButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)

                Label_Text.setToolTip(CommandButton.toolTip())

        # Set the spacing to zero. If not, the CSS styling will show gaps
        Layout.setSpacing(0)
        # Add the layout to the button
        btn.setLayout(Layout)

        # Set the stylesheet
        StyleSheet = StyleMapping.ReturnStyleSheet(control="toolbutton", radius="2px")
        StyleSheet_Addition = """QToolButton::menu-indicator {
                        subcontrol-origin: padding;
                        subcontrol-position: center top;
                    }"""
        CommandButton.setStyleSheet(StyleSheet)
        Label_Text.setStyleSheet(StyleSheet)
        ArrowButton.setStyleSheet(StyleSheet_Addition + StyleSheet)
        btn.setStyleSheet(
            "QToolButton, QToolButton:hover {border: 0.5px solid"
            + StyleMapping.ReturnStyleItem("Background_Color")
            + ";}"
        )
        # Set the final sizes
        #
        # If the text width is smaller than the button, set the extra space to 0
        if TextWidth < ButtonSize.width():
            Space = 0
        ButtonSize = QSize(ButtonSize.width() + Space, ButtonSize.height() + TextHeight)
        CommandButton.setFixedSize(
            QSize(
                CommandButton.width() + Space,
                ButtonSize.height() - MenuButtonSpace - TextHeight - Space,
            )
        )
        btn.setFixedSize(ButtonSize)

        # Return the button
        return btn

    def CustomToolButton(
        Text: str,
        Action: QAction,
        Icon: QIcon,
        IconSize: QSize,
        ButtonSize: QSize,
        FontSize: int = 10,
        showText=True,
        TextAlignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
        TextPositionAlignment=Qt.AlignmentFlag.AlignLeft,
        setWordWrap=True,
        ElideMode=Qt.TextElideMode.ElideNone,
        MaxNumberOfLines=2,
        Menu: QMenu = None,
        MenuButtonSpace=16,
    ):
        # Define the controls
        btn = QToolButton()
        CommandButton = QToolButton()
        ArrowButton = QToolButton()
        Layout = QHBoxLayout()
        Label_Text = QTextEdit()
        # Define the parameters
        TextWidth = 0
        space = 6
        # Remove any trailing spaces
        Text = Text.strip()
        # Set the buttonSize
        CommandButton.setFixedSize(ButtonSize)
        # Set the icon and its size
        CommandButton.setIcon(Icon)
        CommandButton.setIconSize(IconSize)
        # Set the content margins to zero
        CommandButton.setContentsMargins(0, 0, 0, 0)
        # Add a actions if there is only one
        if len(Menu.actions()) == 0:
            CommandButton.addAction(Action)
        CommandButton.setDefaultAction(Action)

        # Define a vertical layout
        Layout = QHBoxLayout()
        # Add the command button
        Layout.addWidget(CommandButton)
        Layout.setAlignment(TextPositionAlignment)
        Font = QFont()
        Font.setPointSize(FontSize)
        Label_Text.setFont(Font)

        # Set the content margins to zero
        Layout.setContentsMargins(0, 0, 0, 0)

        # if showText is False:
        if MenuButtonSpace < 12:
            MenuButtonSpace = 12

        # If text must be shown wrapped, add a layout with label
        if showText is True and Text != "":
            # Create a label
            # Label_Text = QTextEdit()
            Label_Text.setReadOnly(True)
            Label_Text.setFrameShape(QFrame.Shape.NoFrame)
            Label_Text.setFrameShadow(QFrame.Shadow.Plain)
            Label_Text.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            Label_Text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            Label_Text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            Label_Text.document().setDocumentMargin(0)
            Label_Text.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            Label_Text.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            Label_Text.setSizeAdjustPolicy(QTextEdit.SizeAdjustPolicy.AdjustToContents)
            Label_Text.setFixedHeight(CommandButton.height())
            # Set the font
            Font = QFont()
            Label_Text.setFont(Font)
            FontMetrics = QFontMetrics(Font)
            if setWordWrap is True:
                Label_Text.setWordWrapMode(QTextOption.WrapMode.WordWrap)
                # Determine the maximum length per line
                FontMetrics = QFontMetrics(Font)
                maxWidth = 0
                maxLength = 0
                for c in Text:
                    maxWidth = maxWidth + FontMetrics.boundingRectChar(c).width()
                    if maxWidth < ButtonSize.width() * 2:
                        maxLength = maxLength + 1
                    if maxWidth >= ButtonSize.width() * 2:
                        break

                # Get the first text line
                line1 = StandardFunctions.ReturnWrappedText(Text, maxLength, MaxNumberOfLines, True)[0]
                # Add the line with a space to avoid te need to set spacing. (Spacing breaks the hover background)
                Label_Text.append(" " + line1)
                # Try to get the second line if there is one
                try:
                    line2 = StandardFunctions.ReturnWrappedText(Text, maxLength, MaxNumberOfLines, True)[1]
                    # Add the line with a space to avoid te need to set spacing. (Spacing breaks the hover background)
                    Label_Text.append(" " + line2)
                    if FontMetrics.tightBoundingRect(line1).width() > FontMetrics.tightBoundingRect(line2).width():
                        # Update a parameter for the width
                        TextWidth = FontMetrics.tightBoundingRect(line1).width()
                    else:
                        # Update a parameter for the width
                        TextWidth = FontMetrics.tightBoundingRect(line2).width()
                except Exception:
                    # Correct the margin to set the arrow vertical center (bug in Qt)
                    marginCorrection = (CommandButton.height() - FontMetrics.boundingRect(Text).height()) / 2
                    Label_Text.setViewportMargins(0, marginCorrection, 0, 0)
                    # Update a parameter for the width
                    TextWidth = FontMetrics.tightBoundingRect(line1).width()

                # Adjust the size
                Label_Text.setMaximumWidth(TextWidth + space)
                # Update a parameter for the width
                TextWidth = TextWidth + space

            if setWordWrap is False:
                # if the text must be elided, return a updated text
                if ElideMode != Qt.TextElideMode.ElideNone:
                    Text = FontMetrics.elidedText(
                        Text,
                        ElideMode,
                        ButtonSize.width() * 3,
                        Qt.TextFlag.TextSingleLine,
                    )
                    Text = FontMetrics.elidedText(
                        Text,
                        ElideMode,
                        ButtonSize.width() * 3,
                        Qt.TextFlag.TextSingleLine,
                    )
                # Set the number of lines to 1 and disable wrap
                MaxNumberOfLines = 1
                Label_Text.setWordWrapMode(QTextOption.WrapMode.NoWrap)
                # Add the line with a space to avoid te need to set spacing. (Spacing breaks the hover background)
                Label_Text.setText(" " + Text)
                # Update the size
                Label_Text.adjustSize()
                Label_Text.setFixedHeight(CommandButton.height())
                # Correct the margin to set the arrow vertical center (bug in Qt)
                marginCorrection = (CommandButton.height() - FontMetrics.boundingRect(Text).height()) / 2
                Label_Text.setViewportMargins(0, marginCorrection, 0, 0)
                # Update the width parameter
                TextWidth = FontMetrics.boundingRect(Text).width() + space
            # Set the text alignment
            TextAlignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            Label_Text.setAlignment(TextAlignment)
            # Set the margins to zero
            Label_Text.setContentsMargins(0, 0, 0, 0)
            # Add the label with alignment
            Layout.addWidget(Label_Text)

        if Menu is not None and len(Menu.actions()) > 1:
            # Define a menu
            ArrowButton.setMenu(Menu)
            ArrowButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            # Set the height according the space for the menubutton
            ArrowButton.setFixedHeight(CommandButton.height())
            # Set the width according the commandbutton
            ArrowButton.setFixedWidth(MenuButtonSpace)
            ArrowButton.adjustSize()
            # Set the arrow to none. It will be defined via CSS
            ArrowButton.setArrowType(Qt.ArrowType.NoArrow)
            # Set the content margins
            ArrowButton.setContentsMargins(0, 0, 0, 0)
            # Add the Arrow button to the layout
            Layout.addWidget(ArrowButton)

            # Add the label to the area where the user can invoke the menu
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    ArrowButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom(event):
                    BorderColor = StyleMapping.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Label = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 1px solid"
                        + BorderColor
                        + ";border-right: 0px solid"
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;border-top-right-radius: 0px;border-bottom-right-radius: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 1px solid"
                        + BorderColor
                        + ";border-left: 0px solid"
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 0px;border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";}"
                    )
                    if ArrowButton.underMouse():
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    if Label_Text.underMouse():
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                ArrowButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

                # restore the stylesheets on leaving
                def leaveEventCustom(event):
                    StyleSheet = StyleMapping.ReturnStyleSheet(
                        control="toolbutton",
                        radius="2px",
                    )
                    Label_Text.setStyleSheet(StyleSheet)
                    ArrowButton.setStyleSheet(StyleSheet)

                Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
                ArrowButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
        else:
            # Add the label to the area where the user can invoke the menu
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    CommandButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom(event):
                    BorderColor = StyleMapping.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Label = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-left: 0px solid"
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 0px;border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";}"
                    )
                    StyleSheet_Addition_Command = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-right: 0px solid"
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;border-top-right-radius: 0px;border-bottom-right-radius: 0px"
                        + ";}"
                    )
                    if ArrowButton.underMouse():
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    if Label_Text.underMouse():
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                CommandButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

                # restore the stylesheets on leaving
                def leaveEventCustom(event):
                    StyleSheet = StyleMapping.ReturnStyleSheet(
                        control="toolbutton",
                        radius="2px",
                    )
                    Label_Text.setStyleSheet(StyleSheet)
                    CommandButton.setStyleSheet(StyleSheet)

                Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
                CommandButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)

                # Copy the tooltip from the commandbutton to the label
                Label_Text.setToolTip(CommandButton.toolTip())

            # Set the menubutton space to zero because there is no menu
            MenuButtonSpace = 0

        # Set the minimum height for the button
        CommandButton.setMinimumHeight(ButtonSize.height())
        # Set spacing to zero (highlight background will have gaps otherwise)
        Layout.setSpacing(0)

        # Add the layout
        btn.setLayout(Layout)
        # Set the stylesheet for the controls
        StyleSheet = StyleMapping.ReturnStyleSheet(control="toolbutton")
        CommandButton.setStyleSheet(StyleSheet)
        Label_Text.setStyleSheet(StyleSheet)
        ArrowButton.setStyleSheet(StyleSheet)
        # Set the correct dimensions
        btn.setFixedWidth(CommandButton.width() + MenuButtonSpace + TextWidth)
        btn.setFixedHeight(CommandButton.height())

        # return the new button
        return btn
