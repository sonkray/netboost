import os
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class NetBoostApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        
        # Başlık
        title = Label(text="NetBoost - Uygulama Listesi", size_hint_y=None, height=100)
        self.root.add_widget(title)

        # Uygulama Listesi Alanı
        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        self.load_apps()
        
        scroll.add_widget(self.grid)
        self.root.add_widget(scroll)
        return self.root

    def load_apps(self):
        try:
            # Telefondaki 3. parti uygulamaların paket adlarını al
            cmd = "pm list packages -3"
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            packages = output.strip().split('\n')

            for pkg in packages:
                pkg_name = pkg.replace("package:", "").strip()
                
                # Her uygulama için buton oluştur
                btn = Button(
                    text=f"İnterneti Kes: {pkg_name}",
                    size_hint_y=None,
                    height=120
                )
                btn.bind(on_release=lambda x, p=pkg_name: self.block_internet(p))
                self.grid.add_widget(btn)
        except Exception as e:
            self.grid.add_widget(Label(text=f"Hata: {str(e)}", size_hint_y=None, height=100))

    def block_internet(self, pkg_name):
        try:
            # Shizuku/Root üzerinden iptables ile interneti kesme komutu
            cmd = f"su -c 'iptables -I OUTPUT -m owner --uid-owner $(dumpsys package {pkg_name} | grep userId | grep -oE [0-9]+ | head -n 1) -j DROP'"
            os.system(cmd)
            print(f"{pkg_name} için internet kısıtlandı.")
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == '__main__':
    NetBoostApp().run()
