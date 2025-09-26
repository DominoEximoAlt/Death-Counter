import mss
import mss.tools


with mss.mss() as sct:
    
    monitor_number = 1
    mon = sct.monitors[monitor_number]

    # The screen part to capture
    monitor = {
        "top": mon["top"] + 0,  # 100px from the top
        "left": mon["left"] + 400,  # 100px from the left
        "width": 1000,
        "height": 1000,
        "mon": monitor_number,
    }
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)