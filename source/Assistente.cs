using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading;
using System.Windows.Forms;

public class Assistente : Form {
    TextBox disc = new TextBox(), log = new TextBox();
    Button choose = new Button(), prepare = new Button(), play = new Button();
    CheckBox owned = new CheckBox();
    bool busy; Process worker;
    string folder = AppDomain.CurrentDomain.BaseDirectory;
    public Assistente() {
        Text="BAM2 Recomp Test v0.1 — assistente pessoal"; Width=820; Height=610;
        StartPosition=FormStartPosition.CenterScreen;
        var title=new Label{Left=18,Top=16,Width=765,Height=68,
            Text="Use sua imagem original japonesa SLPM-86219 (.cue + .bin).\r\nO pacote nao inclui jogo, BIOS comercial, capa ou codigo gerado do jogo.\r\nRequisitos: Python 3.11+, Git for Windows, internet e espaco livre para compilar."};
        disc.SetBounds(18,92,650,26);choose.SetBounds(680,90,102,28);choose.Text="Selecionar...";
        owned.SetBounds(18,128,760,26);owned.Text="Possuo a copia original e li LEIA-ME.txt e as licencas (uso nao comercial).";
        prepare.SetBounds(18,166,250,36);prepare.Text="1. Preparar minha copia";
        play.SetBounds(280,166,220,36);play.Text="2. Jogar";
        var note=new Label{Left=18,Top=214,Width=760,Height=48,
            Text="A preparacao baixa framework/ferramentas e pode demorar. Dados extraidos,\r\nexecutavel e saves ficam em %LOCALAPPDATA%\\BAM2RecompTest\\v0.1, fora deste pacote."};
        log.SetBounds(18,268,764,285);log.Multiline=true;log.ReadOnly=true;log.ScrollBars=ScrollBars.Both;log.WordWrap=false;
        Controls.AddRange(new Control[]{title,disc,choose,owned,prepare,play,note,log});
        choose.Click+=(s,e)=>{using(var d=new OpenFileDialog{Filter="Imagem CUE|*.cue",CheckFileExists=true}) if(d.ShowDialog()==DialogResult.OK)disc.Text=d.FileName;};
        prepare.Click+=(s,e)=>Start("prepare");play.Click+=(s,e)=>Start("play");
        FormClosing+=(s,e)=>{if(busy){e.Cancel=true;MessageBox.Show("Aguarde o processo terminar. O log informa o progresso.");}};
    }
    static string Quote(string s) {
        var b=new StringBuilder("\"");int slashes=0;
        foreach(char c in s){if(c=='\\'){slashes++;continue;}if(c=='\"'){b.Append('\\',slashes*2+1);b.Append(c);slashes=0;continue;}b.Append('\\',slashes);slashes=0;b.Append(c);}
        b.Append('\\',slashes*2);b.Append('"');return b.ToString();
    }
    void Line(string s) {if(s==null)return;BeginInvoke((Action)(()=>{log.AppendText(s+Environment.NewLine);}));}
    string Python() {
        foreach(string candidate in new[]{"py","python"})try {
            var p=new Process{StartInfo=new ProcessStartInfo(candidate,(candidate=="py"?"-3 ":"")+"-c \"import sys;sys.exit(0 if sys.version_info>=(3,11) else 1)\""){UseShellExecute=false,CreateNoWindow=true}};
            p.Start();if(p.WaitForExit(10000)&&p.ExitCode==0)return candidate;
        }catch{}
        throw new Exception("Python 3.11+ nao encontrado. Instale-o com a opcao de adicionar ao PATH e reabra o assistente.");
    }
    void Start(string action) {
        if(busy)return;
        if(!owned.Checked){MessageBox.Show("Confirme a copia original e a leitura das licencas.");return;}
        if(action=="prepare"&&!File.Exists(disc.Text)){MessageBox.Show("Selecione um arquivo .cue existente.");return;}
        string selected=disc.Text;busy=true;choose.Enabled=prepare.Enabled=play.Enabled=false;
        ThreadPool.QueueUserWorkItem(_=>{
            try {
                string py=Python();string args=(py=="py"?"-3 ":"")+Quote(Path.Combine(folder,"source","prepare.py"))+" "+action;
                if(action=="prepare")args+=" --disc "+Quote(selected);
                worker=new Process{StartInfo=new ProcessStartInfo(py,args){UseShellExecute=false,CreateNoWindow=true,RedirectStandardOutput=true,RedirectStandardError=true,StandardOutputEncoding=Encoding.UTF8,StandardErrorEncoding=Encoding.UTF8}};
                worker.StartInfo.EnvironmentVariables["PYTHONUTF8"]="1";
                worker.StartInfo.EnvironmentVariables["PYTHONUNBUFFERED"]="1";
                worker.OutputDataReceived+=(s,e)=>Line(e.Data);worker.ErrorDataReceived+=(s,e)=>Line(e.Data);
                worker.Start();worker.BeginOutputReadLine();worker.BeginErrorReadLine();worker.WaitForExit();
                Line(worker.ExitCode==0?"Concluido.":"Falhou. Confira o erro acima; a preparacao pode ser tentada novamente.");
            }catch(Exception e){Line("ERRO: "+e.Message);}
            finally{BeginInvoke((Action)(()=>{busy=false;choose.Enabled=prepare.Enabled=play.Enabled=true;}));}
        });
    }
    [STAThread] public static void Main(string[] args) {
        if(args.Length==1&&args[0]=="--self-test") {
            if(Quote("C:\\a b\\")=="\"C:\\a b\\\\\"" && Quote("a\"b")=="\"a\\\"b\"")Environment.Exit(0);
            Environment.Exit(2);
        }
        Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);Application.Run(new Assistente());
    }
}
