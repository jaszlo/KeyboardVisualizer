import ctypes

def get_name_of_virtual_key(virtual_key):
    # Set localization to US English
    ctypes.windll.kernel32.SetThreadLocale.argtypes = [ctypes.c_ulong]
    ctypes.windll.kernel32.SetThreadLocale(1033)
    
    # Get Scancode from Virtual Key and enable LR Distinction for extended key codes
    MAPVK_VK_TO_VSC_EX = 4

    # Call MapVirtualKey to get the character
    # Documentation @ https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeyw
    scan_code = ctypes.windll.user32.MapVirtualKeyW(virtual_key, MAPVK_VK_TO_VSC_EX)
    is_extended_scan_code = scan_code & (0xe1 << 8)
    buffer_size = 255
    buffer = ctypes.create_unicode_buffer(buffer_size)

    # Shift scan code by 16 bits and enable LR Distinction
    scan_code <<= 16
    if is_extended_scan_code:
        # Set bit to enable LR Distinction
        enable_lr_distinction = 1 << 24
        scan_code |= enable_lr_distinction
    # Call GetKeyNameText to get the key name
    # Documentation @ https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getkeynametextw
    _length = ctypes.windll.user32.GetKeyNameTextW(scan_code, buffer, buffer_size)
    # Return string value of buffer
    return buffer.value
