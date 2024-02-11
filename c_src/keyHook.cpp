#include <windows.h>
#include <stdio.h>
#include <locale.h>

// Capitalize umlaute just like all other letters as well
wchar_t * fixGermanUmlauts(wchar_t *key_name) {
    if (wcscmp(key_name, L"ö") == 0) {
        return L"Ö";
    } else if (wcscmp(key_name, L"ä") == 0) {
        return L"Ä";
    } else if (wcscmp(key_name, L"ü") == 0) {
        return L"Ü";
    }
    return key_name;
}

LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode != HC_ACTION) {
        return CallNextHookEx(NULL, nCode, wParam, lParam);
    }

    KBDLLHOOKSTRUCT* pKbStruct = (KBDLLHOOKSTRUCT*)lParam;
    char *prefix = (wParam == WM_KEYDOWN || wParam == WM_SYSKEYDOWN) ? "P-" : "R-";

    // Call MapVirtualKey to get the character
    // Documentation @ https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeyw
    int scan_code = MapVirtualKeyW(pKbStruct->vkCode, MAPVK_VK_TO_VSC_EX);
    int is_extended = scan_code & (0xe1 << 8);
    const int buffer_size = 128;
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
    key_name = fixGermanUmlauts(key_name);
    wprintf(L"%S%ls\n", prefix, key_name);
    fflush(stdout);
    
    // Call the next hook in the chain
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

int main() {

    // Enable UTF-8 Output for AE, OE, UE to be printable
    SetConsoleOutputCP(CP_UTF8);
    setlocale(LC_ALL, "en_US.UTF-8");

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
