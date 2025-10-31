"""
シェルコマンド生成ユーティリティ
"""
from pathlib import Path
from typing import Dict, List

class CodeGenerator:
    """シェルコマンドを生成するクラス"""
    
    @staticmethod
    def generate_powershell_commands(work_dir: str, files: List[Dict]) -> str:
        """PowerShellコマンドを生成"""
        commands = []
        
        # 作業ディレクトリへ移動
        commands.append(f"# 作業ディレクトリへ移動")
        commands.append(f"cd '{work_dir}'")
        commands.append("")
        
        for file_info in files:
            filename = file_info['filename']
            filepath = file_info['filepath']
            content = file_info['content']
            
            # ディレクトリ作成
            dir_path = str(Path(filepath).parent).replace('\\', '/')
            if dir_path and dir_path != '.':
                commands.append(f"# {filename} 用ディレクトリ作成")
                commands.append(f"New-Item -ItemType Directory -Force -Path '{dir_path}' | Out-Null")
                commands.append("")
            
            # ファイル作成
            var_name = filename.replace('.', '_').replace('-', '_')
            commands.append(f"# {filename} を作成")
            commands.append(f"${var_name} = @'")
            commands.append(content)
            commands.append("'@")
            commands.append("")
            commands.append(f"${var_name} | Out-File -FilePath '{filepath}' -Encoding UTF8")
            commands.append("")
            commands.append(f"# 確認")
            commands.append(f"Get-Content '{filepath}' | Select-Object -First 10")
            commands.append("")
            commands.append("# " + "-" * 50)
            commands.append("")
        
        return "\n".join(commands)
    
    @staticmethod
    def generate_terminal_commands(work_dir: str, files: List[Dict]) -> str:
        """Terminal (Mac/Linux) コマンドを生成"""
        commands = []
        
        # 作業ディレクトリへ移動
        commands.append(f"# 作業ディレクトリへ移動")
        commands.append(f"cd '{work_dir}'")
        commands.append("")
        
        for file_info in files:
            filename = file_info['filename']
            filepath = file_info['filepath']
            content = file_info['content']
            
            # ディレクトリ作成
            dir_path = str(Path(filepath).parent)
            if dir_path and dir_path != '.':
                commands.append(f"# {filename} 用ディレクトリ作成")
                commands.append(f"mkdir -p '{dir_path}'")
                commands.append("")
            
            # ファイル作成
            commands.append(f"# {filename} を作成")
            commands.append(f"cat > '{filepath}' << 'EOF'")
            commands.append(content)
            commands.append("EOF")
            commands.append("")
            commands.append(f"# 確認")
            commands.append(f"head -n 10 '{filepath}'")
            commands.append("")
            commands.append("# " + "-" * 50)
            commands.append("")
        
        return "\n".join(commands)
    
    @staticmethod
    def generate_cmd_commands(work_dir: str, files: List[Dict]) -> str:
        """CMD (Windows) コマンドを生成"""
        commands = []
        
        # 作業ディレクトリへ移動
        commands.append(f"REM 作業ディレクトリへ移動")
        commands.append(f"cd /d \"{work_dir}\"")
        commands.append("")
        
        for file_info in files:
            filename = file_info['filename']
            filepath = file_info['filepath'].replace('/', '\\')
            content = file_info['content']
            
            # ディレクトリ作成
            dir_path = str(Path(filepath).parent)
            if dir_path and dir_path != '.':
                commands.append(f"REM {filename} 用ディレクトリ作成")
                commands.append(f"if not exist \"{dir_path}\" mkdir \"{dir_path}\"")
                commands.append("")
            
            # ファイル作成（echoコマンドで行ごとに書き込み）
            commands.append(f"REM {filename} を作成")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if i == 0:
                    commands.append(f"echo {line}> \"{filepath}\"")
                else:
                    commands.append(f"echo {line}>> \"{filepath}\"")
            commands.append("")
            commands.append(f"REM 確認")
            commands.append(f"type \"{filepath}\"")
            commands.append("")
            commands.append("REM " + "-" * 50)
            commands.append("")
        
        return "\n".join(commands)
