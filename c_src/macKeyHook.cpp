#include <ApplicationServices/ApplicationServices.h>
#include <Carbon/Carbon.h>

const char *getControllCharacterName(unsigned short keyCode) {
    switch (keyCode) {
        case kVK_Return:        return "Return";
        case kVK_Tab:           return "Tab";
        case kVK_Space:         return "Space";
        case kVK_Delete:        return "Delete";
        case kVK_Escape:        return "Escape";
        case kVK_Command:       return "Command";
        case kVK_Shift:         return "Shift";
        case kVK_CapsLock:      return "Caps Lock";
        case kVK_Option:        return "Option";
        case kVK_Control:       return "Control";
        case kVK_RightCommand:  return "Right Command";
        case kVK_RightShift:    return "Right Shift";
        case kVK_RightOption:   return "Right Option";
        case kVK_RightControl:  return "Right Control";
        case kVK_UpArrow:       return "Up Arrow";
        case kVK_DownArrow:     return "Down Arrow";
        case kVK_LeftArrow:     return "Left Arrow";
        case kVK_RightArrow:    return "Right Arrow";
        // Add more cases as needed
        default:                return NULL;
    };
}

CGEventRef keyHook(CGEventTapProxy proxy, CGEventType type, CGEventRef event, void *refcon) {
    // Set default Flag 256
    printf("Flag: %llu\n", CGEventGetFlags(event));

    CGEventSetFlags(event, kCGEventFlagMaskNonCoalesced);

    printf("Flag: %llu\n", CGEventGetFlags(event));

    const char *prefix = type == kCGEventKeyDown ? "P-" : "R-";
    // Unset the Modifiers to only have one output for each key
    UniCharCount maxStringLength = 16;
    UniChar unicodeString[maxStringLength];
    UniCharCount actualStringLength;
    
    // Get the Unicode string corresponding to the key code
    CGKeyCode keyCode = (CGKeyCode)CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode);
    const char *specialKeyName = getControllCharacterName(keyCode);
    if (specialKeyName != NULL) {   
        printf("%s%s\n", prefix, specialKeyName);
        return event;
    }

    CGEventKeyboardGetUnicodeString(event, maxStringLength, &actualStringLength, unicodeString);
    if (actualStringLength > 0) {
        printf("%s%lc\n", prefix, unicodeString[0]);
    }

    // Pass the event along
    return event;
}

int main(int argc, const char *argv[]) {
    // Create an event tap
    CFMachPortRef eventTap = CGEventTapCreate(
        kCGSessionEventTap,               // Type of event tap
        kCGHeadInsertEventTap,            // Placement of event tap
        kCGEventTapOptionDefault,         // Options
        // Mask of events to listen for
        CGEventMaskBit(kCGEventKeyDown) 
            //| CGEventMaskBit(kCGEventKeyUp)
            | CGEventMaskBit(kCGEventFlagsChanged),
        keyHook,                    // Callback function
        NULL                              // User data
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
