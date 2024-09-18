
from gi.repository import GObject, Gtk, Gedit, PeasGtk, Gio

import os
import requests
import json


def is_empty_or_whitespace(text):
    # Remove espaços em branco do início e do fim e verifica se a string resultante está vazia
    return not text.strip()

def ler_json_como_dict(filename):
    # Obter o diretório home do usuário
    home_dir = os.path.expanduser("~")
    
    # Construir o caminho completo do arquivo
    caminho_arquivo = os.path.join(home_dir, filename)
    
    # Verificar se o arquivo JSON existe
    if os.path.isfile(caminho_arquivo):
        try:
            # Abrir e carregar o conteúdo do arquivo JSON
            with open(caminho_arquivo, 'r') as json_file:
                data = json.load(json_file)
            return data  # Retornar o conteúdo como dict
        except json.JSONDecodeError:
            print(f"Error decoding file '{caminho_arquivo}'.")
            return None
    else:
        print(f"The file '{caminho_arquivo}' was not found.")
        return None

def escreve_dict_como_json(filename, data):
    # Obter o diretório home do usuário
    home_dir = os.path.expanduser("~")
    
    # Construir o caminho completo do arquivo
    caminho_arquivo = os.path.join(home_dir, filename)
  
    # Criar e salvar o arquivo JSON
    with open(caminho_arquivo, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"The file '{caminho_arquivo}' was created with '{data}'.")
    return True
        
def verifica_ou_cria_json(filename, default_language="en"):
    # Obter o diretório home do usuário
    home_dir = os.path.expanduser("~")
    
    # Construir o caminho completo do arquivo
    caminho_arquivo = os.path.join(home_dir, filename)
    
    # Verificar se o arquivo existe
    if os.path.isfile(caminho_arquivo):
        print(f"The file '{caminho_arquivo}' already exists.")
        return True
    else:
        # Se o arquivo não existe, criar um novo arquivo JSON com a chave "language"
        data = {"language": default_language}
        
        # Criar e salvar o arquivo JSON
        with open(caminho_arquivo, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"The file '{caminho_arquivo}' was created with '{data}'.")
        return False

def send_dict_to_server(server_url,data):
    # Enviar solicitação POST ao servidor
    response = requests.post(f'{server_url}/add_task', json=data)

    if response.status_code == 200:
        print(f"TTS ID: {response.json()['id']}")
        return response.json()['id'];
    else:
        print("Error submitting task to server:", server_url)
        return None

def remove_id_of_server(server_url,task_id):
    # Enviar solicitação DELETE ao servidor
    response = requests.delete(f'{server_url}/remove_task/{task_id}')

    if response.status_code == 200:
        print(response.json()["message"])
        return response.json()["message"]
    else:
        print("Error removing task:",task_id)
        return None

# For our example application, this class is not exactly required.
# But we had to make it because we needed the app menu extension to show the menu.
class ExampleAppActivatable(GObject.Object, Gedit.AppActivatable):
    app = GObject.property(type=Gedit.App)
    __gtype_name__ = "ExampleAppActivatable"

    def __init__(self):
        GObject.Object.__init__(self)
        self.menu_ext = None
        self.menu_item = None
        verifica_ou_cria_json("text_to_speech.json", default_language="en");

    def do_activate(self):
        self._build_menu()

    def _build_menu(self):
        # Get the extension from tools menu        
        self.menu_ext = self.extend_menu("tools-section")
        # This is the submenu which is added to a menu item and then inserted in tools menu.        
        sub_menu = Gio.Menu()
        sub_menu_play   = Gio.MenuItem.new("Play the selected text", 'win.play_selected_text')
        sub_menu.append_item(sub_menu_play)
        sub_menu_remove = Gio.MenuItem.new("Remove the last task", 'win.remove_last_task')
        sub_menu.append_item(sub_menu_remove)
        
        self.menu_item = Gio.MenuItem.new_submenu("Text to speech", sub_menu)
        self.menu_ext.append_menu_item(self.menu_item)
        
        # Setting accelerators, now our action is called when Ctrl+Alt+1 is pressed.
        self.app.set_accels_for_action("win.play_selected_text", ("<Ctrl><Shift>p", None))
        self.app.set_accels_for_action("win.remove_last_task", ("<Ctrl><Shift>r", None))

    def do_deactivate(self):
        self._remove_menu()

    def _remove_menu(self):
        # removing accelerator and destroying menu items
        self.app.set_accels_for_action("win.dictonator_start", ())
        self.menu_ext = None
        self.menu_item = None
        

            



class ExampleWindowActivatable(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    window = GObject.property(type=Gedit.Window)
    __gtype_name__ = "ExampleWindowActivatable"

    def __init__(self):
        GObject.Object.__init__(self)
        # This is the attachment we will make to bottom panel.
        self.bottom_bar = Gtk.Box()
        self.LastID=None;
    
    #this is called every time the gui is updated
    def do_update_state(self):
        # if there is no document in sight, we disable the action, so we don't get NoneException
        if self.window.get_active_view() is not None:
            self.window.lookup_action('play_selected_text').set_enabled(True)
            self.window.lookup_action('remove_last_task').set_enabled(True)

    def do_activate(self):
        # Defining the action which was set earlier in AppActivatable.
        self._connect_menu()
        #self._insert_bottom_panel()

    def _connect_menu(self):
        action_play = Gio.SimpleAction(name='play_selected_text')
        action_play.connect('activate', self.action_cb)
        self.window.add_action(action_play)
    
        action_remove = Gio.SimpleAction(name='remove_last_task')
        action_remove.connect('activate', self.action_rem)
        self.window.add_action(action_remove)
    
    def text_to_speech(self, action):

        view = self.window.get_active_view()
        if not view:
            print("Error: No active view found")
            return

        doc = view.get_buffer()
        start_iter, end_iter = doc.get_selection_bounds()

        if not start_iter or not end_iter:
            print("Error: No selection bounds")
            return

        selected_text = doc.get_text(start_iter, end_iter, False)
        if not selected_text:
            print("Error: No text selected")
            return
        
        info=ler_json_como_dict("text_to_speech.json");
        server_url='http://localhost:5000';
        Dict={ "text": selected_text, "language": info["language"], "split_pattern": ["\n\n","\n\r\n"], "speed":1.25 };
        
        #print(selected_text)
        #print(Dict)
        self.LastID=send_dict_to_server(server_url,Dict);
            
    def action_cb(self, action, data):
        # On action clear the document.
        #doc = self.window.get_active_document()
        #doc.set_text("")
        self.text_to_speech(action)

    def action_rem(self, action, data):
        server_url='http://localhost:5000';
        remove_id_of_server(server_url,self.LastID);

    def _insert_bottom_panel(self):
        # Add elements to panel.
        self.bottom_bar.add(Gtk.Label("Hello There!"))
        # Get bottom bar (A Gtk.Stack) and add our bar.        
        panel = self.window.get_bottom_panel()
        panel.add_titled(self.bottom_bar, 'example', "Example")
        # Make sure everything shows up.
        panel.show()
        self.bottom_bar.show_all()
        panel.set_visible_child(self.bottom_bar)

    def do_deactivate(self):
        self._remove_bottom_panel()

    def _remove_bottom_panel(self):
        panel = self.window.get_bottom_panel()
        panel.remove(self.bottom_bar)

    def do_create_configure_widget(self):
        # Criar uma caixa vertical para a interface de configuração
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Adicionar uma entrada de texto (Gtk.Entry) para o usuário configurar o idioma
        label = Gtk.Label(label="Enter the gtts language code (e.g. 'en' for English):")
        vbox.pack_start(label, False, False, 0)

        info=ler_json_como_dict("text_to_speech.json")

        # Entrada de texto para a configuração do idioma
        self.entry_language = Gtk.Entry()
        self.entry_language.set_text(info['language'])  # Valor padrão
        vbox.pack_start(self.entry_language, False, False, 0)

        # Botão para salvar as configurações
        button = Gtk.Button(label="Save Settings")
        button.connect("clicked", self.on_save_button_clicked)
        vbox.pack_start(button, False, False, 0)

        return vbox
       
    def on_save_button_clicked(self, widget):
        # Quando o botão é clicado, obtemos o texto digitado e salvamos a configuração
        data=dict();
        data['language']=self.entry_language.get_text()
        escreve_dict_como_json("text_to_speech.json", data)
        print(f"Language set to: {data}")
