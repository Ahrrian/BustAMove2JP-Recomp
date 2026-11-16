# Checklist para GitHub — versão fonte-only 0.1

**Status: candidato para revisão, ainda NÃO é autorização jurídica ou release final.**

- [x] Pacote separado do diretório privado de trabalho e da pasta do usuário.
- [x] `Assistente_BAM2.exe` excluído do **pacote fonte-only**; construir localmente.
- [x] `.gitignore` conservador e auditoria com lista explícita de caminhos.
- [x] `manifest-sha256.json` atualizado para todos os arquivos distribuídos.
- [x] Origem, commit, licença e atribuições do PSXRecomp documentados.
- [x] Ausência detectada, na versão revisada, de imagens de disco, músicas,
      executável recompilado do jogo, saves e arquivos C gerados do jogo.
- [x] Delimitado o escopo da MIT para os componentes próprios no NOTICE,
      distinguindo-os dos oito arquivos de runtime sob PolyForm.
- [x] Incluído aviso MIT local de Hyllian/xBR no pacote e preservados os
      links a atribuições oficiais do PSXRecomp no commit fixado.
- [ ] Confirmar a identidade ou designação pública que o mantenedor deseja
      usar em lugar da atribuição coletiva provisória, se desejado, e obter
      autorização de qualquer colaborador humano ou titular terceiro.
- [ ] Revisão jurídica final, se desejada, sobre o uso de código de terceiros,
      alterações do runtime e os direitos pertinentes ao jogo comercial.
- [ ] Decidir se `template/seeds/ghidra_funcs.txt` (588 endereços derivados)
      será divulgado; para política mais restritiva, gerar seeds localmente,
      sem quebrar `prepare.py`.
- [ ] Validar instalação e compilação em Windows limpo usando disco legítimo,
      sem caches ou dependências locais não documentadas.
- [ ] Executar verificação de malware e proveniência antes de distribuir um
      `Assistente_BAM2.exe` compilado; publicar preferencialmente código-fonte.
- [ ] Revisão final do conteúdo real a enviar ao GitHub (`git diff --cached`,
      `git ls-files`, histórico Git limpo). **Não utilizar o histórico do
      diretório privado de desenvolvimento.**
- [ ] Checar possíveis restrições aplicáveis ao jogo/ROM/disco, marcas e leis
      locais. Possuir um disco não é uma autorização universal de distribuição.
- [ ] Executar `py -3 tools\check_publication.py` e confirmar saída OK.

**Atenção:** o verificador identifica nomes, extensões, cabeçalhos binários,
caminhos não aprovados e hashes, mas não garante análise de copyright de
código-fonte arbitrário nem auditoria de segurança completa.
