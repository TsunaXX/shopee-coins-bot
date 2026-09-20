from pathlib import Path
import sys

root = Path(sys.argv[1])

def replace(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    if old not in s:
        raise SystemExit(f"pattern not found in {path}: {old[:120]!r}")
    p.write_text(s.replace(old, new), encoding="utf-8")

# Version bump
replace("app/build.gradle", "versionCode 5", "versionCode 6")
replace("app/build.gradle", "versionName '0.5.0'", "versionName '0.5.1'")

# Fixed explicit light/dark styles: do not depend on values-night resource selection.
(root / "app/src/main/res/values/colors.xml").write_text("""<resources>
    <color name="app_accent_light">#E95F3E</color>
    <color name="app_accent_dark">#FF8A70</color>
    <color name="app_window_bg_light">#FFFFFF</color>
    <color name="app_window_bg_dark">#121212</color>
    <color name="app_status_bg_light">#F4F4F4</color>
    <color name="app_status_bg_dark">#242424</color>
    <color name="app_secondary_text_light">#5F6368</color>
    <color name="app_secondary_text_dark">#B8B8B8</color>
    <color name="app_footer_text_light">#757575</color>
    <color name="app_footer_text_dark">#9E9E9E</color>
    <color name="app_status_bar_light">#FFFFFF</color>
    <color name="app_status_bar_dark">#121212</color>
    <color name="app_nav_bar_light">#FFFFFF</color>
    <color name="app_nav_bar_dark">#121212</color>
</resources>
""", encoding="utf-8")

(root / "app/src/main/res/values/styles.xml").write_text("""<resources>
    <style name="AppThemeLight" parent="android:style/Theme.Material.Light.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:colorAccent">@color/app_accent_light</item>
        <item name="android:windowBackground">@color/app_window_bg_light</item>
        <item name="android:navigationBarColor">@color/app_nav_bar_light</item>
        <item name="android:statusBarColor">@color/app_status_bar_light</item>
        <item name="android:windowLightStatusBar">true</item>
        <item name="android:windowLightNavigationBar">true</item>
    </style>

    <style name="AppThemeDark" parent="android:style/Theme.Material.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:colorAccent">@color/app_accent_dark</item>
        <item name="android:windowBackground">@color/app_window_bg_dark</item>
        <item name="android:navigationBarColor">@color/app_nav_bar_dark</item>
        <item name="android:statusBarColor">@color/app_status_bar_dark</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:windowLightNavigationBar">false</item>
    </style>
</resources>
""", encoding="utf-8")

v31 = root / "app/src/main/res/values-v31"
v31.mkdir(parents=True, exist_ok=True)
(v31 / "colors.xml").write_text("""<resources>
    <color name="app_accent_light">@android:color/system_accent1_600</color>
    <color name="app_accent_dark">@android:color/system_accent1_200</color>
</resources>
""", encoding="utf-8")

# Old night overrides from v0.5 must not affect explicit light/dark mode.
for rel in [
    "app/src/main/res/values-night/colors.xml",
    "app/src/main/res/values-night-v31/colors.xml",
]:
    p = root / rel
    if p.exists():
        p.unlink()

theme = root / "app/src/main/java/com/local/shopeewater/ThemeStore.java"
theme.write_text("""package com.local.shopeewater;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.res.Configuration;

public final class ThemeStore {
    public static final String MODE_SYSTEM = "system";
    public static final String MODE_LIGHT = "light";
    public static final String MODE_DARK = "dark";
    private static final String PREFS = "theme_prefs";
    private static final String KEY_MODE = "mode";

    private ThemeStore() {}

    public static String getMode(Context context) {
        return prefs(context).getString(KEY_MODE, MODE_SYSTEM);
    }

    public static void setMode(Context context, String mode) {
        if (!MODE_LIGHT.equals(mode) && !MODE_DARK.equals(mode)) {
            mode = MODE_SYSTEM;
        }
        prefs(context).edit().putString(KEY_MODE, mode).apply();
    }

    public static boolean isDark(Context context) {
        String mode = getMode(context);
        if (MODE_DARK.equals(mode)) return true;
        if (MODE_LIGHT.equals(mode)) return false;
        int mask = context.getResources().getConfiguration().uiMode
                & Configuration.UI_MODE_NIGHT_MASK;
        return mask == Configuration.UI_MODE_NIGHT_YES;
    }

    public static void apply(Activity activity) {
        activity.setTheme(isDark(activity) ? R.style.AppThemeDark : R.style.AppThemeLight);
    }

    public static int color(Context context, int lightRes, int darkRes) {
        return context.getColor(isDark(context) ? darkRes : lightRes);
    }

    private static SharedPreferences prefs(Context context) {
        return context.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }
}
""", encoding="utf-8")

main = root / "app/src/main/java/com/local/shopeewater/MainActivity.java"
s = main.read_text(encoding="utf-8")
s = s.replace(
    'V0.5 Final｜Shizuku 直連＋雙排程＋深色／系統主題',
    'V0.5.1 Final｜Shizuku 直連＋雙排程＋深色／系統主題'
)
s = s.replace(
    'getColor(R.color.app_status_bg)',
    'ThemeStore.color(this, R.color.app_status_bg_light, R.color.app_status_bg_dark)'
)
s = s.replace(
    'getColor(R.color.app_secondary_text)',
    'ThemeStore.color(this, R.color.app_secondary_text_light, R.color.app_secondary_text_dark)'
)
s = s.replace(
    'getColor(R.color.app_footer_text)',
    'ThemeStore.color(this, R.color.app_footer_text_light, R.color.app_footer_text_dark)'
)
s = s.replace(
    'V0.5 Final 保留 V0.4 已驗證的 Shizuku 澆水、指定時間／間隔排程、鎖定通知與解鎖補澆核心；本版只收尾外觀與版本資訊。',
    'V0.5.1 Final 修正手動切換淺色／深色時與系統 night 資源互相干擾；Shizuku 澆水與排程核心維持 V0.4／V0.5 不變。'
)
main.write_text(s, encoding="utf-8")

(root / "README.md").write_text("""# 蝦蝦果園快速澆水 V0.5.1 Final

V0.5.1 是 V0.5 Final 的外觀修正版。

- 修正手機系統為深色時，App 手動選「淺色」仍套到夜間色彩資源，造成黑字／深色背景混用。
- 跟隨系統、固定淺色、固定深色三種模式互不干擾。
- Android 12+ 保留系統桌布動態重點色。
- Shizuku 澆水、指定時間排程、間隔排程、鎖定通知與解鎖補澆核心不變。
- versionCode 6 / versionName 0.5.1。
""", encoding="utf-8")
