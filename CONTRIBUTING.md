# Guia de Contribuição

## Fluxo de desenvolvimento

O projeto utiliza uma estratégia baseada em Trunk-Based Development.

A branch "main" é protegida e não deve receber alterações diretamente.

Toda alteração deve ser o fluxo:

Criar uma branch a partir da "main";
Realizar as alterações;
Fazer commits;
Enviar a branch ao GitHub;
Abrir um pull request para a "main";
Aguardar a revisão e aprovação do PR;
Realizar o merge somente após as validações terminarem.

## Padrão de branches

"feature/" - nova funcionalidade
"fix/" - correções
"test/" - testes
"infra/" - infraestrutra e DevOps
"docs/" - documentação

## Padrão dos commits

Utilizamos o estilo Conventional Commits:

"feat" - nova funcionalidade
"fix" - correção
"test" - testes
"ci" - integração contínua
"docs" - documentação
"chore" - configuração ou manutenção
"refactor" - refatoraçãomkdir -p .github