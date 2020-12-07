# Coletor de Ceps
    Projeto criado para pegar um cep da tabela do banco de dados e coletar o endereço completo no site dos correios,
    atualizando o registro no banco de dados novamente. Necessário ter os ceps cadastrados no banco de dados. 
    A estrutura utilizada para a tabela do cep está abaixo.

## Tabela do banco
    `CREATE TABLE `cep` (
        `codigo` bigint NOT NULL AUTO_INCREMENT,
        `cep` varchar(50) NOT NULL,
        `logradouro` varchar(500) DEFAULT NULL,
        `complemento` varchar(120) DEFAULT NULL,
        `bairro` varchar(120) DEFAULT NULL,
        `localidade` varchar(120) DEFAULT NULL,
        `uf` varchar(2) DEFAULT NULL,
        `ibge` varchar(120) DEFAULT NULL,
        `gia` varchar(120) DEFAULT NULL,
        `ddd` varchar(3) DEFAULT NULL,
        `siafi` varchar(120) DEFAULT NULL,
        `ativo` tinyint(1) NOT NULL DEFAULT '1',
        PRIMARY KEY (`codigo`)
    ) ENGINE=InnoDB AUTO_INCREMENT=732764 DEFAULT CHARSET=utf8;

## Pacotes necessários para o funcionamento: ##
    - pip3 install PyMySQL
    - pip3 install selenium

## Antes de Rodar abra a pasta do projeto com seu editor. ##
    - Instale os pacotes necessários.
    - Altere na linha 17 o usuário e senha do seu banco Mysql.
    - Altere na linha 33 o caminho do arquivo geckodriver.
    
## Como executar?
    Utilizo a versão 3 do python.
    Entrar na pasta do projeto via terminal e executar o comando python3 coletor.py cep inicial e final. 
    python3 coletor.py 1 2000


    
