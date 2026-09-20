from pathlib import Path
import sys

root = Path(sys.argv[1])
main = root / "app/src/main/java/com/local/shopeewater/MainActivity.java"
gradle = root / "app/build.gradle"

s = main.read_text(encoding="utf-8")
s = s.replace(
    "測試版 0.1｜手機解鎖且螢幕亮起時自動執行",
    "測試版 0.2｜手機解鎖且螢幕亮起時自動執行"
)
s = s.replace(
    'Button termuxPermission = button("授權 Termux 執行權限");',
    'Button termuxPermission = button("設定 Termux 執行權限");'
)
s = s.replace(
    '        if (!TermuxRunner.hasPermission(this)) requestTermuxPermission();\n',
    ''
)

old = '''    private void requestTermuxPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            requestPermissions(new String[]{TermuxRunner.RUN_COMMAND_PERMISSION}, REQ_TERMUX);
        }
    }
'''

new = '''    private void requestTermuxPermission() {
        if (TermuxRunner.hasPermission(this)) {
            Toast.makeText(this, "Termux 執行權限已授權", Toast.LENGTH_SHORT).show();
            return;
        }

        new AlertDialog.Builder(this)
                .setTitle("設定 Termux 執行權限")
                .setMessage(
                        "這個權限是由 Termux 提供的額外權限。Android 15 上不一定會跳出一般權限視窗。\\n\\n" +
                        "請開啟本 App 的：\\n" +
                        "應用程式資訊 → 權限 → 額外權限\\n\\n" +
                        "再允許「Run commands in Termux environment」/「在 Termux 環境中執行命令」。\\n\\n" +
                        "完成後返回 App，狀態會自動更新。")
                .setPositiveButton("開啟 App 資訊", (d, which) -> openOwnAppSettings())
                .setNeutralButton("嘗試系統授權", (d, which) -> {
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                        requestPermissions(new String[]{TermuxRunner.RUN_COMMAND_PERMISSION}, REQ_TERMUX);
                    }
                })
                .setNegativeButton("取消", null)
                .show();
    }

    private void openOwnAppSettings() {
        try {
            Intent i = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                    Uri.parse("package:" + getPackageName()));
            startActivity(i);
        } catch (Exception e) {
            Intent fallback = new Intent(Settings.ACTION_MANAGE_APPLICATIONS_SETTINGS);
            startActivity(fallback);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQ_TERMUX) {
            refreshStatus();
            if (TermuxRunner.hasPermission(this)) {
                Toast.makeText(this, "Termux 執行權限已授權", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "若沒有出現授權視窗，請使用「開啟 App 資訊」手動允許額外權限", Toast.LENGTH_LONG).show();
            }
        }
    }
'''

if old not in s:
    raise SystemExit("requestTermuxPermission block not found")

s = s.replace(old, new)
main.write_text(s, encoding="utf-8")

g = gradle.read_text(encoding="utf-8")
g = g.replace("versionCode 1", "versionCode 2")
g = g.replace("versionName '0.1.0'", "versionName '0.2.0'")
gradle.write_text(g, encoding="utf-8")
