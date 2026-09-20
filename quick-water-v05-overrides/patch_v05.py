from pathlib import Path
import sys

root = Path(sys.argv[1])

def replace(path, old, new):
    p = root / path
    s = p.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'pattern not found in {path}: {old[:80]!r}')
    p.write_text(s.replace(old, new), encoding='utf-8')

replace('app/build.gradle', 'versionCode 4', 'versionCode 5')
replace('app/build.gradle', "versionName '0.4.0'", "versionName '0.5.0'")
replace('app/src/main/AndroidManifest.xml', 'android:theme="@style/AppTheme"', 'android:theme="@style/AppThemeLight"')

p = root / 'app/src/main/java/com/local/shopeewater/MainActivity.java'
s = p.read_text(encoding='utf-8')
s = s.replace('import android.graphics.Typeface;\n', 'import android.graphics.Typeface;\nimport android.content.res.Configuration;\n')
s = s.replace('import android.view.ViewGroup;\n', 'import android.view.ViewGroup;\nimport android.util.TypedValue;\n')
s = s.replace('    private Switch intervalSwitch;\n', '    private Switch intervalSwitch;\n    private Spinner themeModeSpinner;\n')
s = s.replace('    private boolean autoRunHandled = false;\n', '    private boolean autoRunHandled = false;\n    private boolean updatingTheme = false;\n')
s = s.replace('    protected void onCreate(Bundle savedInstanceState) {\n        super.onCreate(savedInstanceState);', '    protected void onCreate(Bundle savedInstanceState) {\n        ThemeStore.apply(this);\n        super.onCreate(savedInstanceState);')
s = s.replace('root.addView(text("蝦蝦果園快速澆水", 26, true));\n        TextView subtitle = text("穩定版 0.4｜Shizuku 直連＋指定時間／間隔排程", 14, false);\n        subtitle.setTextColor(Color.DKGRAY);', 'root.addView(text("蝦蝦果園快速澆水", 26, true));\n        TextView subtitle = text("V0.5 Final｜Shizuku 直連＋雙排程＋深色／系統主題", 14, false);\n        subtitle.setTextColor(getColor(R.color.app_secondary_text));')
s = s.replace('statusText.setBackgroundColor(Color.rgb(246, 246, 246));', 'statusText.setBackgroundColor(getColor(R.color.app_status_bg));')
s = s.replace('hint.setTextColor(Color.DKGRAY);', 'hint.setTextColor(getColor(R.color.app_secondary_text));')
s = s.replace('intervalHint.setTextColor(Color.DKGRAY);', 'intervalHint.setTextColor(getColor(R.color.app_secondary_text));')
old = '''        Button save = button("儲存速度設定");
        save.setOnClickListener(v -> saveDelays());
        root.addView(save, marginTop(10));

        TextView footer = text(
                "V0.4 保留 V0.3 實機通過的 Shizuku shell 流程與相對座標；間隔排程會在每次成功澆水或待解鎖補澆完成後重新計時。",
                12,
                false);
        footer.setTextColor(Color.GRAY);
        root.addView(footer, marginTop(18));
'''
new = '''        Button save = button("儲存速度設定");
        save.setOnClickListener(v -> saveDelays());
        root.addView(save, marginTop(10));

        root.addView(section("外觀"), marginTop(22));
        TextView themeHint = text(
                "可跟隨系統切換淺色／深色。Android 12 以上會自動套用系統桌布的動態重點色。",
                13,
                false);
        themeHint.setTextColor(getColor(R.color.app_secondary_text));
        root.addView(themeHint, marginTop(4));

        themeModeSpinner = new Spinner(this);
        ArrayAdapter<String> themeAdapter = new ArrayAdapter<>(
                this,
                android.R.layout.simple_spinner_item,
                new String[]{"跟隨系統", "淺色", "深色"});
        themeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        themeModeSpinner.setAdapter(themeAdapter);
        themeModeSpinner.setOnItemSelectedListener(new android.widget.AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(android.widget.AdapterView<?> parent, View view, int position, long id) {
                if (updatingTheme) return;
                String mode = position == 1 ? ThemeStore.MODE_LIGHT
                        : position == 2 ? ThemeStore.MODE_DARK
                        : ThemeStore.MODE_SYSTEM;
                if (!mode.equals(ThemeStore.getMode(MainActivity.this))) {
                    ThemeStore.setMode(MainActivity.this, mode);
                    recreate();
                }
            }

            @Override
            public void onNothingSelected(android.widget.AdapterView<?> parent) {}
        });
        root.addView(themeModeSpinner, marginTop(8));

        TextView footer = text(
                "V0.5 Final 保留 V0.4 已驗證的 Shizuku 澆水、指定時間／間隔排程、鎖定通知與解鎖補澆核心；本版只收尾外觀與版本資訊。",
                12,
                false);
        footer.setTextColor(getColor(R.color.app_footer_text));
        root.addView(footer, marginTop(18));
'''
if old not in s: raise SystemExit('footer block not found')
s = s.replace(old, new)
old = '''        if (intervalUnitSpinner != null) {
            intervalUnitSpinner.setSelection("minutes".equals(ScheduleStore.getIntervalUnit(this)) ? 0 : 1);
        }

        renderSchedules();
'''
new = '''        if (intervalUnitSpinner != null) {
            intervalUnitSpinner.setSelection("minutes".equals(ScheduleStore.getIntervalUnit(this)) ? 0 : 1);
        }

        if (themeModeSpinner != null) {
            updatingTheme = true;
            String mode = ThemeStore.getMode(this);
            themeModeSpinner.setSelection(ThemeStore.MODE_LIGHT.equals(mode) ? 1
                    : ThemeStore.MODE_DARK.equals(mode) ? 2 : 0);
            updatingTheme = false;
        }

        renderSchedules();
'''
if old not in s: raise SystemExit('refresh block not found')
s = s.replace(old, new)
s = s.replace('empty.setTextColor(Color.GRAY);', 'empty.setTextColor(getColor(R.color.app_footer_text));')
s = s.replace('v.setTextColor(Color.rgb(30, 30, 30));', 'v.setTextColor(themeColor(android.R.attr.textColorPrimary, Color.rgb(30, 30, 30)));')
s = s.replace('l.setTextColor(Color.DKGRAY);', 'l.setTextColor(getColor(R.color.app_secondary_text));')
old = '''    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
'''
new = '''    private int themeColor(int attr, int fallback) {
        TypedValue value = new TypedValue();
        if (!getTheme().resolveAttribute(attr, value, true)) return fallback;
        if (value.resourceId != 0) {
            try {
                return getColor(value.resourceId);
            } catch (Throwable ignored) {}
        }
        return value.data != 0 ? value.data : fallback;
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
'''
if old not in s: raise SystemExit('dp block not found')
s = s.replace(old, new)
p.write_text(s, encoding='utf-8')

(root / 'app/src/main/java/com/local/shopeewater/ThemeStore.java').write_text('''package com.local.shopeewater;

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
    public static String getMode(Context context) { return prefs(context).getString(KEY_MODE, MODE_SYSTEM); }
    public static void setMode(Context context, String mode) {
        if (!MODE_LIGHT.equals(mode) && !MODE_DARK.equals(mode)) mode = MODE_SYSTEM;
        prefs(context).edit().putString(KEY_MODE, mode).apply();
    }
    public static void apply(Activity activity) {
        String mode = getMode(activity);
        boolean dark;
        if (MODE_DARK.equals(mode)) dark = true;
        else if (MODE_LIGHT.equals(mode)) dark = false;
        else {
            int mask = activity.getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK;
            dark = mask == Configuration.UI_MODE_NIGHT_YES;
        }
        activity.setTheme(dark ? R.style.AppThemeDark : R.style.AppThemeLight);
    }
    private static SharedPreferences prefs(Context context) {
        return context.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }
}
''', encoding='utf-8')

(root / 'app/src/main/res/values/styles.xml').write_text('''<resources>
    <style name="AppThemeLight" parent="android:style/Theme.Material.Light.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:colorAccent">@color/app_accent</item>
        <item name="android:windowBackground">@color/app_window_bg</item>
        <item name="android:navigationBarColor">@color/app_nav_bar</item>
        <item name="android:statusBarColor">@color/app_status_bar</item>
        <item name="android:windowLightStatusBar">true</item>
        <item name="android:windowLightNavigationBar">true</item>
    </style>
    <style name="AppThemeDark" parent="android:style/Theme.Material.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:colorAccent">@color/app_accent</item>
        <item name="android:windowBackground">@color/app_window_bg</item>
        <item name="android:navigationBarColor">@color/app_nav_bar</item>
        <item name="android:statusBarColor">@color/app_status_bar</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:windowLightNavigationBar">false</item>
    </style>
</resources>
''', encoding='utf-8')

(root / 'app/src/main/res/values/colors.xml').write_text('''<resources>
    <color name="app_accent">#E95F3E</color>
    <color name="app_window_bg">#FFFFFF</color>
    <color name="app_status_bg">#F4F4F4</color>
    <color name="app_secondary_text">#5F6368</color>
    <color name="app_footer_text">#757575</color>
    <color name="app_status_bar">#FFFFFF</color>
    <color name="app_nav_bar">#FFFFFF</color>
</resources>
''', encoding='utf-8')
night = root / 'app/src/main/res/values-night'; night.mkdir(parents=True, exist_ok=True)
(night / 'colors.xml').write_text('''<resources>
    <color name="app_accent">#FF8A70</color>
    <color name="app_window_bg">#121212</color>
    <color name="app_status_bg">#242424</color>
    <color name="app_secondary_text">#B8B8B8</color>
    <color name="app_footer_text">#9E9E9E</color>
    <color name="app_status_bar">#121212</color>
    <color name="app_nav_bar">#121212</color>
</resources>
''', encoding='utf-8')
v31 = root / 'app/src/main/res/values-v31'; v31.mkdir(parents=True, exist_ok=True)
(v31 / 'colors.xml').write_text('''<resources>
    <color name="app_accent">@android:color/system_accent1_500</color>
</resources>
''', encoding='utf-8')
n31 = root / 'app/src/main/res/values-night-v31'; n31.mkdir(parents=True, exist_ok=True)
(n31 / 'colors.xml').write_text('''<resources>
    <color name="app_accent">@android:color/system_accent1_200</color>
</resources>
''', encoding='utf-8')

(root / 'README.md').write_text('''# 蝦蝦果園快速澆水 V0.5 Final

V0.5 Final 以 V0.4 穩定核心為基礎，只做介面與版本收尾。

- Shizuku 直連澆水、立即澆水、指定時間與間隔排程維持不變。
- 鎖定時保留一筆待補澆，解鎖後由通知補澆。
- 外觀可選跟隨系統／淺色／深色。
- Android 12+ 自動使用系統桌布的動態重點色。
- 不繞過 PIN、圖形、密碼或生物辨識鎖定。
''', encoding='utf-8')
