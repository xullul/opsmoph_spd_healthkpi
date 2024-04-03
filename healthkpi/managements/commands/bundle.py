import glob
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from typing import Any, Tuple


class Command(BaseCommand):
    help = 'transpile typescript with Babel and bundle with ESBuild'
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        root: Path = settings.BASE_DIR
        
        if hasattr(settings, 'JS_DIRS'):
            jsdirs: Tuple[Path, ...] = settings.JS_DIRS
        else:
            raise CommandError(
                'Cannot find JS_DIRS in settings. '
                'Make sure you have a JS_DIRS as "Tuple" containing "Path" objects in your settings. '
                'The path must be a directory containing "src" and "dist" directories'
            )
        
        corejs = Path('node_modules/core-js/')
        babel = root / Path('node_modules/.bin/babel')
        esbuild = root / Path('node_modules/.bin/esbuild')
        targets = '--target=chrome58,firefox57,safari11,edge16'
        outdir = root / Path('healthkpi/static/healthkpi/js/dist/')
        
        # make sure core-js is installed
        if corejs.exists() == False:
            raise CommandError(
                f'Cannot find core-js in "{str(corejs)}". '
                'Are you forget to install core-js? '
                'Run "pnpm i" or "pnpm install". '
                'Make sure you init pnpm and have core-js'
                'included in package.json. If not, run "pnpm add core-js"'
            )
        
        # make sure babel is installed
        if babel.exists() == False:
            raise CommandError(
                f'Cannot find babel at "{str(babel)}". 
                Are you forget to install babel? '
                'Run "pnpm i" or "pnpm install". '
                'Make sure you init pnpm and have @babel/core, @babel/cli, @babel/preset-env and @babel/preset-typescript'
                'included in package.json. If not, run '
                '"pnpm add --save-dev @babel/core @babel/cli @babel/preset-env @babel/preset-typescript"'
            )
        
        if esbuild.exists() == False:
            raise CommandError(
                f'Cannot find esbuild at "{str(esbuild)}". 
                Are you forget to install esbuild? '
                'Run "pnpm i" or "pnpm install". '
                'Make sure you init pnpm and have esbuild included in package.json. If not, run '
                '"pnpm add --save-exact --save-dev esbuild"'
            )
        
        for jsdir in jsdirs:
            # make sure directories exists
            if jsdir.exists() == False:
                jsdir.mkdir(777, parents=True, exist_ok=True)
            
            src = jsdir / 'src/'
            dist = jsdir / 'dist/'
            
            if src.exists() == False:
                src.mkdir(777, parents=True, exist_ok=True)
            
            if dist.exists() == False:
                dist.mkdir(777, parents=True, exist_ok=True)
            
            src_files = glob.glob(str(src / '*.ts'))
            dist_files = glob.glob(str(dist / '*.js'))
            
            # transpile to old ecmascript version and polyfill with babel + corejs
            if len(src_files) > 0:
                for ts in src_files:
                    command = f'{babel} {ts} --out-dir {outdir}'
                    self.stdout.write(command)
                    subprocess.run(command, shell=True, check=True, encoding='utf-8')
                self.stdout.write('transpile .ts files finished', self.style.SUCCESS)
            else:
                self.stdout.write(f'no .ts files found in "{str(src)}"')
            
            # bundle with esbuild to run on browser
            if len(dist_files) > 0:
                for js in dist_files:
                    command = f'{esbuild} {js} --bundle --platform=node  {targets} --outdir={outdir}'
                    self.stdout.write(command)
                    subprocess.run(command, shell=True, check=True, encoding='utf-8')
            else:
                self.stdout.write(f'no .js files found in "{str(dist)}"')
            
            self.stdout.write('bundle javascript files successfully', self.style.SUCCESS)