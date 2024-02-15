#include <ApplicationServices/ApplicationServices.h>
#include <Carbon/Carbon.h>
#include <wchar.h>

const char *getControllCharacterName(unsigned short keyCode) {
    switch (keyCode) {
        case kVK_F1:                return "F1";
        case kVK_F2:                return "F2";
        case kVK_F3:                return "F3";
        case kVK_F4:                return "F4";
        case kVK_F5:                return "F5";
        case kVK_F6:                return "F6";
        case kVK_F7:                return "F7";
        case kVK_F8:                return "F8";
        case kVK_F9:                return "F9";
        case kVK_F10:                return "F10";
        case kVK_F11:                return "F11";
        case kVK_F12:                return "F12";
        case kVK_ANSI_Equal:        return "Akut";
        case kVK_ANSI_Minus:        return "ß";
        case kVK_ANSI_Semicolon:    return "ö";
        case kVK_ANSI_Quote:        return "ä";
        case kVK_ANSI_LeftBracket:  return "ü";
        case kVK_Return:            return "Return";
        case kVK_Tab:               return "Tab";
        case kVK_Space:             return "Space";
        case kVK_Delete:            return "Delete";
        case kVK_Escape:            return "Escape";
        case kVK_Command:           return "Command";
        case kVK_Shift:             return "Shift";
        case kVK_CapsLock:          return "Caps Lock";
        case kVK_Option:            return "Option";
        case kVK_Control:           return "Control";
        case kVK_RightCommand:      return "Right Command";
        case kVK_RightShift:        return "Right Shift";
        case kVK_RightOption:       return "Right Option";
        case kVK_RightControl:      return "Right Control";
        case kVK_UpArrow:           return "Up Arrow";
        case kVK_DownArrow:         return "Down Arrow";
        case kVK_LeftArrow:         return "Left Arrow";
        case kVK_RightArrow:        return "Right Arrow";
        // Add more cases as needed
        default:                    return NULL;
    };
}


// Store pressed state as controll characters are not sent as key down/up events
const uint VK_COUNT = 256;
bool vkPressed[VK_COUNT];

CGEventRef keyHook(CGEventTapProxy proxy, CGEventType type, CGEventRef event, void *refcon) {
    CGKeyCode keyCode = (CGKeyCode)CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode);
    // Update vkPressed if type is kCGEventFlagsChanged
    if (type == kCGEventFlagsChanged) {
        vkPressed[keyCode] = !vkPressed[keyCode];
    }
    // Determin if pressed or released
    const char *prefix = (type == kCGEventKeyDown || vkPressed[keyCode]) ? "P-" : "R-";

    // Get the Unicode string corresponding to the key code
    
    // Skip FN key
    if (keyCode == kVK_Function || keyCode == 179) {
        return event;
    }
    
    const char *specialKeyName = getControllCharacterName(keyCode);
    if (specialKeyName != NULL) {   
        printf("%s%s\n", prefix, specialKeyName);
        fflush(stdout);
        return event;
    }

    TISInputSourceRef currentKeyboard = TISCopyCurrentKeyboardInputSource();
    CFDataRef layoutData = (CFDataRef)TISGetInputSourceProperty(currentKeyboard, kTISPropertyUnicodeKeyLayoutData);
    if (layoutData == NULL) {
        // printf("Unable to get keyboard layout data.\n");
        return event;
    }

    const UCKeyboardLayout *keyboardLayout = (const UCKeyboardLayout *)CFDataGetBytePtr(layoutData);
    UniCharCount maxStringLength = 255;
    UniChar unicodeString[maxStringLength];
    UniCharCount actualStringLength;
    UInt32 deadKeyState = 0;

    OSStatus status = UCKeyTranslate(
        keyboardLayout,
        keyCode,
        kUCKeyActionDown,
        kCGEventFlagMaskNonCoalesced,
        LMGetKbdType(),
        kUCKeyTranslateNoDeadKeysMask,
        &deadKeyState,
        maxStringLength,
        &actualStringLength,
        unicodeString
    );

    if (status != noErr) {
        // printf("Unable to determine the key name.\n");
        return event;
    } 

    unicodeString[actualStringLength] = '\0';
    printf("%s%s\n", prefix, (char *)unicodeString);
    fflush(stdout);
    CFRelease(currentKeyboard);
    return event;
}

int main(int argc, const char *argv[]) {
    // Initialize vkPressed with nothing being pressed
    for (uint i = 0; i < VK_COUNT; i++) {
        vkPressed[i] = false;
    }

    // Create an event tap
    CFMachPortRef eventTap = CGEventTapCreate(
        kCGSessionEventTap,               // Type of event tap
        kCGHeadInsertEventTap,            // Placement of event tap
        kCGEventTapOptionDefault,         // Options
        // Mask of events to listen for
        CGEventMaskBit(kCGEventKeyDown) 
            | CGEventMaskBit(kCGEventKeyUp)
            | CGEventMaskBit(kCGEventFlagsChanged),
        keyHook,                    // Callback function
        NULL                        // User data
    );

    if (eventTap == NULL) {
        printf("Could not register Key Hook");
        return 1;
    }

    // Create a run loop source
    CFRunLoopSourceRef runLoopSource = CFMachPortCreateRunLoopSource(
        kCFAllocatorDefault, eventTap, 0
    );

    // Add the run loop source to the current run loop
    CFRunLoopAddSource(CFRunLoopGetCurrent(), runLoopSource, kCFRunLoopCommonModes);

    // Enable the event tap
    CGEventTapEnable(eventTap, true);

    // Run the run loop
    CFRunLoopRun();

    // Cleanup
    CFRelease(eventTap);
    CFRelease(runLoopSource);

    return 0;
}
