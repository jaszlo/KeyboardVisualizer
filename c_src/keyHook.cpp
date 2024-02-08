#include <windows.h>
#include <stdio.h>

/*
 * This is a quote from the windows header file:
 * VK_0 - VK_9 are the same as ASCII '0' - '9' (0x30 - 0x39)
 * 0x3A - 0x40 : unassigned
 * VK_A - VK_Z are the same as ASCII 'A' - 'Z' (0x41 - 0x5A)
 */
bool isAlphaNumeric(int vkCode) {
    return (0x30 <= vkCode && vkCode <= 0x39) || (vkCode >= 0x41 && vkCode <= 0x5A);
}

LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode != HC_ACTION) {
        return CallNextHookEx(NULL, nCode, wParam, lParam);
    }

    char *prefix = (wParam == WM_KEYDOWN) ? "Press-" : "Release-";

    KBDLLHOOKSTRUCT* pKbStruct = (KBDLLHOOKSTRUCT*)lParam;
    // Check for Controll Keys
    switch (pKbStruct->vkCode) {
        case VK_TAB:
            printf("%sTab\n", prefix);
            break;
        case VK_CAPITAL:
            printf("%sCaps\n", prefix);
            break;
        case VK_LSHIFT:
        case VK_RSHIFT:
        case VK_SHIFT:
        case MK_SHIFT:
            printf("%sShift\n", prefix);
            break;
        case VK_LCONTROL:
        case VK_RCONTROL:
        case VK_CONTROL:
        case MK_CONTROL:
            printf("%sCtrl\n", prefix);
            break;
        // Function keys F1-F3
        case VK_F1:
        case VK_F2:
        case VK_F3:
            printf("%sF%d\n", prefix, pKbStruct->vkCode - VK_F1 + 1);
            break;
        case VK_ESCAPE:
            printf("%sEsc\n", prefix);
            break;
        case VK_SPACE:
            printf("%sSpace\n", prefix);
            break;
        default:
            // Alphanumerical keys
            if (isAlphaNumeric(pKbStruct->vkCode)) {
                printf("%s%c\n", prefix, pKbStruct->vkCode);
            }
    }

    // Flush stdout so if run as subprocess from main.py, the output is immediately available
    fflush(stdout);

    // Call the next hook in the chain
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}


int main() {
    // Set up low-level keyboard hook
    HHOOK hook = SetWindowsHookEx(WH_KEYBOARD_LL, LowLevelKeyboardProc, GetModuleHandle(NULL), 0);

    if (hook == NULL) {
        // Handle hook setup failure
        printf("Could not register Key Hook");
        return 1;
    }
    // Message loop to keep the program running
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0) != 0) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // Unhook the keyboard hook before exiting
    UnhookWindowsHookEx(hook);
    return 0;
}
