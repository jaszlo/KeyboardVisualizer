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

    KBDLLHOOKSTRUCT* pKbStruct = (KBDLLHOOKSTRUCT*)lParam;
    char *prefix = (wParam == WM_KEYDOWN || wParam == WM_SYSKEYDOWN) ? "Press-" : "Release-";

    // Call MapVirtualKey to get the character
    // Documentation @ https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeyw
    int scan_code = MapVirtualKeyW(pKbStruct->vkCode, MAPVK_VK_TO_VSC_EX);    
    int is_extended = pKbStruct->flags & LLKHF_EXTENDED;
    const int buffer_size = 64;
    wchar_t buffer[buffer_size];

    // Shift scan code by 16 bits and enable LR Distinction to prepare for GetKeyNameTextW
    scan_code <<= 16;
    if (is_extended) {
        int enable_lr_distinction = 1 << 24;
        scan_code |= enable_lr_distinction;
    }

    // Call GetKeyNameText to get the key name
    // Documentation @ https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getkeynametextw
    int length = GetKeyNameTextW(scan_code, buffer, buffer_size);
    wchar_t *key_name = _wcsdup(buffer);
    printf("%s%ls\n", prefix, key_name);
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
