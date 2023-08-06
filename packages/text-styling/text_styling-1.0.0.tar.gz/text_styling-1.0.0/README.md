# Módulo "text_styling"
Esse pacote contém módulo com cores e estilos para texto.<br>
Ele é útil, pois se toda hora tivessemos que escrever `\033[<Código de cor>m`, nosso código ficaria muito poluído.<br>
Por isso esse pacote facilita a estilização dos textos em Python.<br>

## Índice
- [Módulo "text\_styling"](#módulo-text_styling)
  - [Índice](#índice)
  - [módulo "colors"](#módulo-colors)
    - [Variáveis disponíveis](#variáveis-disponíveis)
    - [Exemplo](#exemplo)
  - [módulo "background"](#módulo-background)
- [](#)
    - [Exemplo](#exemplo-1)
  - [módulo "styles"](#módulo-styles)
- [](#-1)
    - [Exemplo](#exemplo-2)
  - [Contate-me](#contate-me)

## módulo "colors"
Esse módulo do pacote contém variáveis para cor do texto.<br>

### Variáveis disponíveis
As variáveis disponíveis no módulo são:
<ul>
    <li>reset</li>
    <li>black</li>
    <li>red</li>
    <li>green</li>
    <li>yellow</li>
    <li>blue</li>
    <li>magenta</li>
    <li>cyan</li>
    <li>white</li>
    <li>inversion</li>
</ul>

### Exemplo
``` python
# Forma padrão
print("\033[31mEste texto está em vermelho\033[m")
```

``` python
# Usando o módulo "colors"
from text_styling.colors import red, reset

print(f"{red}Este texto está em vermelho{reset}")
```

Saída:

<font color="red"><pre>Este texto está em vermelho</pre></font>

## módulo "background"
Esse módulo do pacote contém variáveis para cor do fundo do texto.<br>

#
As variáveis disponíveis no módulo são:
<ul>
    <li>bg_reset</li>
    <li>bg_black</li>
    <li>bg_red</li>
    <li>bg_green</li>
    <li>bg_yellow</li>
    <li>bg_blue</li>
    <li>bg_magenta</li>
    <li>bg_cyan</li>
    <li>bgwhite</li>
</ul>

### Exemplo
``` python
# Forma padrão
print("\033[41mEste texto está em vermelho\033[m")
```

``` python
# Usando o módulo "background"
from text_styling.background import bg_red, reset

print(f"{bg_red}Este texto está com o fundo vermelho{reset}")
```

Saída:

<pre style="background-color: red">Este é um texto com fundo vermelho</pre>

## módulo "styles"
Esse módulo do pacote contém variáveis para estilo de texto.<br>

#
<ul>
    <li>reset</li>
    <li>bold</li>
    <li>small</li>
    <li>italic</li>
    <li>underlined</li>
</ul>

### Exemplo
``` python
# Forma padrão
print("\033[3mEste texto está em itálico\033[m")
```

``` python
# Usando o módulo "styles"
from text_styling.styles import italic, reset

print(f"{italic}Este texto está em itálico{reset}")
```

Saída:

<pre style="font-style: italic">Este texto está em itálico</pre>

## Contate-me
Para relatar problemas ou me contatar, mande um e-mail para **_viniciusmarcelinosilva1983@ gmail.com_**, sempre respondo.