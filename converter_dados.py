import re
import sqlite3

# Dados brutos fornecidos pelo usuário
raw_data = """
LOJA OUTLET ABC-12 loja
LOJA - PARÁ DE MINAS ABC-123 Tulio Amaral
LOJA OUTLET ABC-128 Priscila
LOJA -DIVINOPOLIS ABC-131 Leandro
FRANQ. - VIÇOSA ABC137 franquia - viçosa Windows 8.1
FRANQ. - VIÇOSA ABC-142 franquia - viçosa
MATRIZ ABC-150 Geiziane Bonoto
LOJA CATALÃO ABC-153 LOJA
MATRIZ - RH ABC-159 Maura Bianca "maura.bianca@abcdaconstrucao.com.br" S
LOJA PARA DE MINAS ABC-161
LOJA DIVINOPOLIS ABC-162
Ubá ABC-163 Eliane de Paula eliane.pereira@abcdaconstrucao.com.br Sim Windowns 10 Pro
LOJA CATALÃO -BH ABC-176 Ana Beatriz anabeatriz.pinto@abcdaconstrucao.com.br Caixa Sim Windowns 10 Pro
MATRIZ - Monitor ABC-196
LOJA CATALÃO ABC-207
CD - MINAS ABC218 RESERVA Windows 8.1
CD - MINAS ABC222 Windows 8.1
LOJA JOQUEI ABC-226 DEPRECIADA
LOJA JOQUEI ABC-229 adriana adriana@abcdaconstrucao.com.br loja Windowns 10 Pro
FRANQ. - VIÇOSA ABC-230 Windows 7
CD - MINAS ABC236 RESERVA Windows 8.1
CD - MINAS ABC-237 Robô Compras PCE
CD - MINAS ABC-242 Windows 8.1
LOJA OUTLET ABC245 DEPRECIADA
LOJA JOQUEI ABC246 loja - Vendedora Roberta
LAVRAS ABC-247
CD - MINAS ABC-251 Robô Compras COMPRA
LOJA SPAZIO ABC-252
LOJA CATALÃO ABC-254 loja Windowns 10 Pro
LOJA DIVINOPOLIS ABC-258
CD - MINAS ABC-259 COMPRA Windows 8
CD - MINAS ABC-261 RESERVA
LOJA UBA ABC-262 Gilson Martins gilson.martins@abcdaconstrucao.com.br Windowns 10 Pro
LOJA DIVINOPOLIS ABC263 Bot CDM Windows 8
LOJA DIVINOPOLIS ABC-264
LOJA DIVINOPOLIS ABC-265
LOJA DIVINOPOLIS ABC266 DEPRECIADA
LOJA DIVINOPOLIS ABC-267 DEPRECIADA
FILIAL - DIVINÓPOLIS ABC-268 Raquel Alves raquel.alves@abcdaconstrucao.com.br
LOJA CATALÃO ABC269
LOJA UBA ABC-270
CD - MINAS ABC271 RESERVA
CD - MINAS ABC-272 COMPRA
CD - MINAS ABC277 Juliana Galvani juliana.galvani@abcdaconstrucao.com.br COMPRA Windows 8.1
CDA - VARGINHA ABC-279 Fábio - Gerente Varginha varginha.cda@abcdaconstrucao.com.br S
MATRIZ - LOJA ABC-280 Josiane Ferreira josianeferreira@abcdaconstrucao.com.br S Windowns 10 Pro
LOJA JOQUEI ABC-295 Yuri Souza yuri.souza@abcdaconstrucao.com.br Windowns 10 Pro
MATRIZ ABC-299 robô Ti
LOJA CATALÃO -BH ABC-303 Area de vendas
LOJA CATALÃO ABC-305
LOJA CATALÃO ABC-306 Windows 8
ABC-307 Windows 7
LOJA CATALÃO ABC-310 Roberta Titonele roberta.titonele@abcdaconstrucao.com.br Windowns 10 Pro
LOJA CATALÃO ABC-311
FRANQ. - CATAGUASES ABC-312
CD - MINAS ABC-315 Heverton Silva heverton.silva@abcdaconstrucao.com.br DPTO DE TRANSPORTE Windowns 10 Pro
CD - MINAS ABC-318 RESERVA
CD - MINAS ABC-319 RESERVA
CDA - JD CANADA ABC-320 DEPRECIADA
LOJA UBA ABC-328 Josiel Roque de Oliveira josiel.oliveira@abcdaconstrucao.com.br
LOJA SÃO PEDRO ABC-329 Windows 8.1
LOJA OUTLET ABC-330
LOJA OUTLET ABC-331
LOJA PARA DE MINAS ABC-332 Windows 7
Para de Minas ABC-334 Sabrina sabrina.santos@abcdaconstrucao.com.br Vendas
LOJA OUTLET ABC-336
ABC-340
CD - MINAS ABC-342
CD - MINAS ABC343
CD - MINAS ABC-344 FATOR-SI
MATRIZ - LOJA - EXPEDIÇÃO ABC-350 Heitor Christian / Gustavo Diogo N/A S Windowns 10 Pro
LOJA DIVINOPOLIS ABC-362 Windows 7
LOJA PARA DE MINAS ABC-363 Rodrigo Seldeira Windowns 10 Pro
MATRIZ - TESOURARIA ABC-367 Robô (Financeiro) S
LOJA PARA DE MINAS ABC-368
LOJA PARA DE MINAS ABC-369 Caixa
LOJA LAFAIETE ABC-376
LOJA PARA DE MINAS ABC-379 Sabrina Santos sabrina.santos@abcdaconstrucao.com.br
LOJA NOVA SERRANA ABC-380
LOJA SPAZIO ABC392
LOJA NOVA SERRANA ABC-397
ABC-398 Ana Carolina Cesário "matriz.adm1@abcdaconstrucao.com.br" S
CD - MINAS ABC-399 MEA
LOJA NOVA SERRANA ABC-404
LOJA NOVA SERRANA ABC-406
MATRIZ - LOJA ABC-408 Marcelo Teixeira S
MATRIZ - TI - MONITORAMENTO ABC-418 Fabio Teotônio S
LOJA UBA ABC-422 Windows 8.1 DEPRECIADA
LOJA SPAZIO ABC-423 Monica Horta monicahorta@abcdaconstrucao.com.br Windows 8.1
CDA - RESENDE ABC-424
LAVRAS ABC-426
MATRIZ - LOJA ABC440 Geral S
CD - MINAS ABC-447 FPP
LOJA SÃO PEDRO ABC-454 OSMAR
LOJA CATALÃO ABC-458
LOJA CATALÃO - DIRETOR ABC461
MATRIZ - FINANCEIRO ABC-465 Natália Alberti
LOJA OUTLET ABC-467 Gilson Diretoria
MATRIZ - VENDA EXTERNA ABC-469 Bianca Melo vendaexterna S
MATRIZ - TESOURARIA ABC-472 BRJ742KFLW Romario Elias romario. Contas a Pagar S WIN10 Note pertecia ao Jefferson Soares
Matriz -TI ABC-473 Matriz T.I Sim Windows 10 Pro Equip. adquirido da vivo
UBÁ ABC-474 GILVAN FRANÇA gilvan.franca@abcdaconstrucao.com.br Gerencia SIM WIN10
CD Minas - FEP ABC-476 ST:48R2QK2 Roberta Vantine roberta.vantine@abcdaconstrucao.com.br FEP SIM WIN10
CD - MINAS ABC-477
CD NOVA LIMA ABC-478 980706 CD NOVA LIMA SIM WIN10 MAQUINA CD DE NOVA LIMA
LOJA SPAZIO ABC-479
Conselheiro Lafaiete ABC-480 Giovana Rezende giovana.rezende@abcdaconstrucao.com.br Loja SIM WIN10
Contas a Pagar ABC-481 Nelma Sanabio
CD - MINAS ABC-482
MATRIZ - FINANCEIRO ABC-484 Anderson de Paula andersondepaula
MATRIZ - CONTABILIDADE ABC-485 Yanka Oliveira
ABC487
MATRIZ - Pós Vendas ABC-488 PE04HB6Y Livia Pires livia.pires@abcdaconstrucao.com.br Pós Vendas SIM Windows 11 Pro
ABC-489
Matriz ABC-491 TI NÃO Ubuntu 20.04.3 LTS abc@491#
ABC-492
CD - MINAS ABC-494 PE04S9MM Renan Silva renan.silva@grupomysa.com.br Transporte Sim Win 11
CD - MINAS ABC495 PE04S8D3 BACKUP SIM WIN10 Máquina de backup
CD - MINAS ABC496
CD - MINAS ABC-497 PE04MRQY Kleyverson Jesus kleyverson.jesus@abcdaconstrucao.com.br PCL Sim Windows 11
CD Minas - Compras ABc-498 Kauã Magrini kaua.magrini@abcdaconstrucao.com.br Compras Sim Windowns 10 Pro
CD - MINAS ABC-499 LENOVO Leonardo Neto leonardo.neto@abcdaconstrucao.com.br Almoxarifado sIM Windows 11
ABC501
CD - MINAS ABC-502 Operação otavio.souza@abcdaconstrucao.com.br
MATRIZ - RH ABC-503 Samuel Souza Assis S
MATRIZ - RH ABC-504 Roberta Pereira N
Nova Lima - Expansão ABC505-NB BRJ9516ZLV Guilherme Santana guilherme.santana@abcdaconstrucao.com.br Expansão Sim Windowns 10 Pro
ABC506-NB
ABC-507 BRJ001754f
CD - MINAS ABC508
ABC-509
CD - MINAS ABC510 BRJ0088913 Carlos Clara carlos.clara@abcdaconstrucao.com.br Contabilidade Sim Windows 11 Pro
ABC511
Growth ABC512 BRJ0088902 Jessica Simões jessica.simoes@abcdaconstrucao.com.br Growth S Win10
Pós venda - CDM ABC-515 6YH01LA#AC4 Jessica Merces jessica.merces@abcdaconstrucao.com.br Pós Venda Sim Windowns 10
CDA ABC-517 CDA Divinopolis
CD - MINAS ABC-518
ABC-519
MATRIZ - ABC-521 Viviane Ferreira viviane.ferreira@abcdaconstrucao.com.br CAF Sim Windows 11 Pro Notebook Lenovo
MATRIZ - VENDA EXTERNA ABC-522 Moacir Andrade vendaexterna S
CD - MINAS ABC-523
CD - MINAS ABC-524
ABC-525
Matriz ABC-526
Auditoria - Matriz ABC-527 Arthur Fernandes arthur.fernandes@abcdaconstrucao.com.br Auditoria Sim Windows 10 Pro
ABC-528
ABC-529
ABC530
ABC531
ABC-532
ABC-533
CD Minas - FEP ABC-534 21470048031 Joice Nascimento joice.nascimento@abcdaconstrucao.com.br Qualidade E Auditoria Sim Windows 11 Pro
ABC535
CDA Guarulhos ABC536 BV2PN33 Katia Silva katia.silva@plenalogistica.com.br Transporte Sim Windows 11 Pro
CD - MINAS ABC537 803PN33 Marcos Perdigão marcos.perdigao@abcdaconstrucao.com.br MEA sim Windowns 11 Pro
CD - MINAS ABC538 Leonardo Rafael Simões Operação
ABC539
CD - MINAS ABC540 6V2PN33 Dilly Fator SI dilly.fatorsi@abcdaconstrucao.com.br Transporte Sim Windows 11 Entregue
ABC-543
CD - MINAS ABC-544 BRJ039D3NF Hellony Pinto hellony.pinto@abcdaconstrucao.com.br PPP sim Windowns 11 Pro
CD - MINAS ABC545 Larissa Transporte Sim WIN10
ABC-546
Matriz ABC-547 2SCL263 Isabela Fernandes isabela.fernandes@abcdaconstrucao.com.br CSC Sim Windowns 11 Pro
CD - MINAS ABC-548 CRCL263 Jefferson Ferreira jefferson.ferreira@abcdaconstrucao.com.br MEA DPTO DE MOVIMENTACAO E ARMAZENAGEM sim Windows 11 pro
Outlet - Joquei ABC-549 PE05JPEG Fabiano Oliveira fabiano.oliveira@abcdaconstrucao.com.br vendas Sim Windows 11 pro
CD - MINAS ABC-550 Yasmin Silva yasmin.silva@abcdaconstrucao.com.br ENTRADA NOTAS S
MATRIZ - FINANCEIRO ABC-551 Lívia Freitas livia.freitas@abcdaconstrucao.com.br Contabilidade Sim Windowns 10
CD - MINAS ABC552
MATRIZ - Pos Venda ABC553 Geralys Hurtado geralys.hurtado@abcdaconstrucao.com.br Pós Vendas sim win 11
ABC-554 giulia.pereira win 11
CD - MINAS ABC-555 Victor Piazzi Pos Vendas
CD - MINAS ABC-556
CD - MINAS ABC-557
CD - MINAS ABC-558
CD - MINAS ABC-559
CD - MINAS ABC-560
MATRIZ - FINANCEIRO ABC-561 Maristella Cabral
CD - MINAS ABC-562
MATRIZ ABC-563
MATRIZ - LOJA ABC-564 Roberto Lima S
LOJA MURIAE ABC-565
LOJA PORTO BELLO ABC-566
LOJA JOQUEI ABC-567
CD - MINAS ABC-568 D19F873 Sandro Rangel sandro@abcdaconstrucao.com.br MEA DPTO DE MOVIMENTACAO E ARMAZENAGEM sim Windows 11 pro
MATRIZ - JURÍDICO ABC-569 Rodrigo Silva S
LOJA DIVINOPOLIS ABC-570
MATRIZ ABC-571
MATRIZ ABC-572
LOJA PORTO BELLO ABC-573
MATRIZ - LOJA ABC-574 Francisco Filho "francisco.filho@abcdaconstrucao.com.br" S
CD - MINAS ABC-575
CD - MINAS ABC-576 Operação / Bipagem
LOJA LAFAIETE - CAIXA ABC-577
LOJA LAFAIETE ABC578
LOJA LAFAIETE ABC-579
CDA Montes Claros ABC-580 9W8F873 Marcus Santos marcus.santos@plenalogistica.com.br Transporte Sim Windows 10 Pro
CD - MINAS ABC-581
LOJA PORTO BELLO ABC-582
LOJA MURIAE ABC583
CD Minas ABC-584 BRJ044DPNP Marcos Costa marcos.costa@abcdaconstrucao.com.br TI PO Sim Windows 11 Pro
CD - MINAS ABC-585
ABC-586
CD - MINAS ABC-587 Wesley Schuina wesley.schuina@abcdaconstrucao.com.br PPP sim Windowns 11 Pro
LOJA MURIAE ABC-588
LOJA MURIAE ABC-589
LOJA MURIAE ABC-590
LOJA MURIAE ABC-591
CD - MINAS ABC-592 8MU94LA- HP Yasmin Oliveira yasmin.oliveira@grupomysa.com.br Transporte S WIN 11
ABC-593
LOJA SJDR ABC-594
LOJA SJDR ABC-595
LOJA SJDR ABC-596
LOJA SJDR ABC-597
Compras ABC-598 565RB93 Alexandre Delgado alexandre.delgado@abcdaconstrucao.com.br Compras Sim Windows 11 Pro
LOJA LAVRAS ABC-599
LOJA LAVRAS ABC-600
LOJA LAVRAS ABC-601
LOJA LAVRAS ABC-602
Matriz - Tesouraria ABC-603 Cynthia
LOJA LAVRAS ABC-604
CDM ABC-605 43390230591 sim Windows 11 pro
MATRIZ ABC-607 TI SIM WIN 10
ABC-608 Gustavo Gayer
CD - MINAS ABC-609
FATOR ABC-610 BWKF873 Pedro Augusto Araújo pedro.araujo@abcdaconstrucao.com.br FATOR SIM Windows 11
CD- MINAS ABC-611 4WKF873 CÁSSIA DOS SANTOS GUIMARÃES cassia.guimaraes@abcdaconstrucao.com.br TPP SIM Windowns 11 Pro
ABC-612 765RB93
MATRIZ - DBA ABC-613 Gleidison Andrade
CD - Minas - Transporte ABC-614 Maiara Candido maiara.candido@abcdaconstrucao.com.br Transporte Sim Windows 11 pro
ABC-615 Wanderlei Silva
ABC616
ABC617 Filipe Tedesco filipe.tedesco@abcdaconstrucao.com.br FEP Sim Windowns 11 Pro
CD - MINAS ABC618 Pos Vendas
CD - MINAS ABC619 6Y8F873 Yasmin Cardoso yasmin.cardoso@abcdaconstrucao.com.br FEP Sim Windowns 11 Pro
CD - MINAS ABC-620
ABC-621
ABC-622 faturamentoecommerce@abcdaconstrucao.com.br S
CDA - IPATINGA -MG ABC-623 Cleone CDA's
ABC-624
CD - MINAS ABC-625 DW8F873 Arthur Calixto arthur.calixto@abcdaconstrucao.com.br PCE Sim Win 11
MATRIZ - FINANCEIRO ABC-626 Ingrid Torres ingrid.torres@abcdaconstrucao.com.br Financeiro Sim Windows 10 Pro
CD - MINAS ABC-627 COMPRAS
CD - MINAS ABC-628
LOJA UBA ABC-629 João Bertolato joao.bertolato@abcdaconstrucao.com.br Vendas
LOJA SPAZIO ABC-630
ABC-631
LOJA SPAZIO ABC-632
LOJA SPAZIO ABC-633
LOJA OUTLET ABC-634
LOJA OUTLET ABC-635
LOJA SÃO PEDRO ABC-636
LOJA UBA ABC-637
LOJA UBA ABC-638
LOJA SÃO PEDRO ABC-639
LOJA SÃO PEDRO ABC-640
CD - MINAS ABC-641 Nathalia PPP Windows 10 Máq. BlackFriday foi encaminhada para setor de PPP no CD.
CD-MINAS-PPP ABC-643 BRJ048FD2T Hayane Luz Boldrini hayane.boldrini@abcdaconstrucao.com.br PPP sim Windowns 11 Pro
CD - MINAS ABC-644 BRJ048FC61 GABRIEL SURIANI gabriel.suriani@abcdaconstrucao.com.br M&A SIM WINDOWS 11 ESTAGIÁRIO HP
ABC-645
LOJA SJDR ABC-646
LOJA OUTLET ABC-647
LOJA OUTLET ABC-648
LOJA OUTLET ABC-649
CD - MINAS ABC-650 Cavalcante ailton.cavalcante@abcdaconstrucao.com.br Vendas Lojinha N Windows 10
ABC651
MATRIZ - FINANCEIRO ABC-652 Vanderson Fortes estagiario.financeiro
MATRIZ - FINANCEIRO ABC-653 Santana santana@abcdaconstrucao.com.br Contas a Paga Sim Windows 10 Pro
ABC-654
CD - MINAS ABC-656
CD - MINAS ABC-657
CD - MINAS ABC-658 Lyo Oliveira lyo.oliveira@abcdaconstrucao.com.br PCE Windows 10 Pro
Matriz - Contas a Pagar ABC-659 BRJ051FXP8 Carla Patricia carla.patricia@abcdaconstrucao.com.br Contas a Pagar sim Windowns 11 Pro A máquina esta sendo usada pelos colaboradores - Yago Quintieri / Alice Hermenegildo
MATRIZ ABC-660
BH - Capacitação ABC-661
ABC-662
MATRIZ - pos venda ABC-663 nicole.dornelas nicole.dornelas@abcdaconstrucao.com.br
Matriz - Pós Vendas ABC-664 ST: 30YS0D3 Nathaly Vitória nathaly.vitoria@abcdaconstrucao.com.br Pós Vendas Sim Windowns 11 Pro
Transporte ABC-665 ST:258G1D3 Bruno Nascimento bruno.nascimento@abcdaconstrucao.com.br Transporte sim Windowns 11 Pro
ABC-666
CD - MINAS ABC-667 Maria Eduarda Sá mariaeduarda.sa@grupomysa.com.br
CD - MINAS ABC-668
Loja Joquei Club ABC-669 3ws7wc3
MATRIZ - LOJA ABC-670 "Robison Ribeiro" matriz.gerente@abcdaconstrucao.com.br S
CDA JACAREÍ-SP ABC-671 Denilson Francisco de Araujo CD MINAS
ABC-672
MATRIZ ABC-673 ST:10YS0D3 Sybele Castro sybele.castro@abcdaconstrucao.com.br RH Sim WIN10
CD - MINAS ABC-674
CD - MINAS ABC-675
CD - MINAS ABC-676
CD - MINAS ABC-677
CD - MINAS ABC-678
MATRIZ - RH ABC-679 Douglas Fortes S
CD - MINAS ABC-680 Lara Assis
MATRIZ - RH ABC-681 Kinston José "rh.admissao@abcdaconstrucao.com.br" N
CD - MINAS ABC-682 Thacya Almeida CAF
CD - MINAS ABC-683 ewerton.neves ewerton.neves@abcdaconstrucao.com.br contabilidade sim Windowns 11 Pro
CD - MINAS ABC-684 Jessica Vieira Faturamento Home-Office
CD - MINAS ABC-685 Marcos Novaes marcos.novaes@abcdaconstrucao.com.br Operação Mea
LOJA PORTO BELLO ABC-686 Marcia Telefone da loja (3232-6155)
CD-MINIAS-PPP ABC-687 WESLEY SCHUINA wesley.schuina@abcdaconstrucao.com.br PPP SIM Windowns 11 Pro PPP
ABC-688 ""
MATRIZ - CAF ABC-689 Roberta
CD Minas - FEP ABC-690 Ana Carolina Martines "anacarolina.martines@abcdaconstrucao.com.br" Faturamento Sim Windowns 10 Pro
MATRIZ - LOJA - CAIXA ABC-691 Silvana Nogueira "matriz.adm2@abcdaconstrucao.com.br" S
CD - MINAS ABC-692 4LQTVD3 Marcos Perdigão marcos.perdigao@abcdaconstrucao.com.br MEA Sim Windowns 11 Pro
MATRIZ - Expansão ABC-693 Diego Pedroso
CD - MINAS ABC-694
CD - MINAS ABC-695 Rebeca Borges Dos Reis Vieira rebeca.vieira@abcdaconstrucao.com.br Qualidade E Auditoria Sim Windowns 11 Pro
MATRIZ - LOJA ABC-696 Reinaldo Richard S
ABC-697
CD - MINAS - sesmt ABC-698 2GR0TD3 Bruna Soares bruna.soares@abcdaconstrucao.com.br Compras Sim Windowns 11 Pro
CD - MINAS Financeiro ABC-699 BGR0TD3 Kevin Ramirez kevin.ramirez@abcdaconstrucao.com.br Financeiro Sim Windows 11 Pro
MATRIZ - JURÍDICO ABC-700 Anderson Henriques S
CD - MINAS ABC-701 Jefferson Silva VENDA CORPORATIVA S
CD - MINAS ABC-702 jessica.nascimento jessica.nascimento@abcdaconstrucao.com.br
CD - MINAS ABC-703 Felipe Ribeiro felipe.ribeiro@abcdaconstrucao.com.br DP Sim Windows 10 Pro
Matriz -CSC ABC-704 CFY16Q3 Marcio Oliveira marcio.oliveira@abcdaconstrucao.com.br
CD - MINAS ABC-705 Daniel Carvalho Compras Compras
CD - MINAS ABC-706 Fabricio Resende fabricio.resende@abcdaconstrucao.com.br Expansão sim Windowns 11 Pro
MATRIZ - FINANCEIRO ABC-707 Anderson de Paula
ABC-708
CAF - CONSULTOR ABC-709 Jackson Mauricio
ABC-710
Fabio Ramos ABC-711 ST:5Z0VQD3 Fabio Ramos fabio.ramos@abcdaconstrucao.com.br DEV Sim Ubuntu Senha.: ABC#711@
MATRIZ - TESOURARIA ABC-712 Lara Oliveira S
CD Minas ABC-713 ST:5SB5CF3 Fabio Fernandes fabio.fernandes@abcdaconstrucao.com.br Fator Si sim windowns 11 Pro
MATRIZ - TI - Seg Info ABC-714 DPB2MF3 Anderson José de Souza anderson.souza@abcdaconstrucao.com.br Qualidade sim Windowns 11 Pro
MATRIZ - TI - Seg Info ABC-715 Mariana de Sales Tomaz mariana.tomaz@abcdaconstrucao.com.br S
MATRIZ - CONTAS A PAGAR ABC-716 Marcia Filgueiras marciafilgueiras@abcdaconstrucao.com.br S
ABC-717
MATRIZ ABC-718
CAF ABC720 Gabriela Silva gabriela.silva@abdaconstrucao.com.br CAF SIM Windows 10
CD - MINAS ABC-721 Mayara Silva mayara.silva@abcdaconstrucao.com.br Marketplace Sim
CD - MINAS ABC-722 st:5d52mf3 Brendha Espinosa Pos Vendas
CD - MINAS ABC-723 Ana Luiza Campos analuiza.campos@abcdaconstrucao.com.br Monitoramento sim Windowns 11 Pro
CD - MINAS ABC-724
Muriaé ABC-725 FKSXMF3 Gustavo Simão gustavo.simao@abcdaconstrucao.com.br vendas SIM Windowns 11 Pro
CD - MINAS ABC-726
CD - MINAS ABC-727
CD - MINAS ABC-728
CD - MINAS ABC-729 Esmael FATOR SI WIND10
MATRIZ ABC-730 143186154876KSXNF3 ANA MENDES FEP SIM WIN10
CURITIBS - PR ABC-731 André Melo andre.melo@abcdaconstrucao.com.br DEV Não Ubuntu 20.04.3 LTS Lxn731#
CD - MINAS ABC-732 C8NRQF3 Bernardo Ottoni bernardo.ottoni@abcdaconstrucao.com.br TI SIm WIN 11 Pro
CD - MINAS ABC-733 B8NRQF3 Arthur Sabino arthur.sabino@abcdaconstrucao.com.br M&a Sim Windows 11
Capacitação ABC-734 ST: 88NRQF3 William Canaan william.canaan@abcdaconstrucao.com.br Capacitação Sim Windows 10 pro
MATRIZ ABC-735
Marketing - Gerente ABC-736
EXpansão ABC-737 ST:48NRQF3 reinan.santos reinan.santos@abdaconstrucao.com.br Expansão sim
Pós Venda - CDM ABC-738 ST: 38NRQF3 Larissa Nogueira larissa.nogueira@abcdaconstrucao.com.br Pós Vendas Sim Windows 11 Pro
CD - MINAS ABC-739
CD - MINAS ABC-740 Beatriz Transporte
CD - MINAS ABC-741 9992MF3 GABRIEL MEURER gabriel.meurer@abcdaconstrucao.com.br SIM WIN 11
CD - MINAS ABC-742 SIM WIN 11
CD - MINAS ABC-743
Groth - BH ABC-744
CD - MINAS ABC-745
Secretária ABC-746
CD - MINAS ABC-747
Matriz - Gerente ABC-748 Robison
CD - MINAS ABC-749 MOSTRUARIO
MATRIZ-fi ABC-750 ST:68NRQF3 vania.nascimento vania.nascimento@abcdaconstrucao.com.br ERP sim WIN 11 Pro
CD - MINAS ABC-751 ST:7R2C5G3 estephani.almeida@abcdaconstrucao.com.br
CD - MINAS ABC-752
CD - MINAS ABC-753 DP2C5G3 Marco Antonio Carpanez marco.carpanez@grupomysa.com.br Transporte Silm WIN 11 Pro
CD - MINAS ABC-754
TI NELIO ABC-755
Diretor - RH ABC-756
CD Minas ABC-757 7S9PXG3 Bernardo Ottoni bernardo.ottoni@abcdaconstrucao.com.br TI Sim Windows 11 Pro
Expansão ABC-758
Expansão ABC-759
MATRIZ - POS VENDA ABC-760 Camilly.santos Camilly.santos@abcdaconstrucao.com.br sim WIN 11 Pro
Muriaé ABC-761 BP8PXG3 Ricardo Peixoto ricardo.peixoto@abcdacpnstrucao.com.br Lojas Propria Sim Windows 11 Pro
CD - MINAS ABC-762 4Q8PXG3 Rebeca Vieira rebeca.vieira@abcdaconstrucao.com.br Qualidade sim Windowns 11 Pro
CD - MINAS ABC-763 Laura Lopes laura.lopes@abcdaconstrucao.com.br RH Sim Windowns 11 Pro
CD - MINAS ABC-764
Outlet ABC-765
Outlet ABC-766
Marketing ABC-767 24366 Phaison phaison@abcdacontrucao.com.br Win10
CD - MINAS ABC-768 1Q8PXG3 Gabriel Barbosa gabriel.barbosa@abcdaconstrucao.com.br Farming/Marketplace Sim Windows 11 Troca pela Lenovo
ABC-769
ABC-770
RH ABC-771
ABC-772 3333668
MATRIZ - Vendas ABC-773
CD MINAS - Transporte ABC-774 CP8PXG3 Felipe Teixeira felipe.teixeira@abcdaconstrucao.com.br Transporte Sim Windows 11 Pro
Rodrigo Oliveira ABC-775 3333668 LUCIANO SANTOS rodrigo.oliveiras@abcdaconstrucao.com.br TRANSPORTE WIN10
RH - Kinston José ABC-776
Jacqueline ABC-777 ST: JP8PXG3 tayna.ferreira@abcdaconstrucao.com.br RH sim Windowns 11 Pro
CDA Ribeirão Preto - Ronie Von ABC-778
Financeiro - Rafael Indiani ABC-779 ST:2Q8PXG3 3333668 Rafel Indiani rafael.indiani@abcdaconstrucao.com.br Fiscal WIN10
ABC-780
Loja Muriaé ABC-781 ST: HP8PXG3 3333668 Ricardo Peixoto ricardo.peixoto@abcdacpnstrucao.com.br Gerente loja Muriaé Sim WIN10 Garantia expira em 13/08/2022
TI - ERP ABC-782 ST:6P8PXG3 3333668 Carolina Laurindo carolina.vitoria@abcdaconstrucao.com.br TI- ERP Sim Windws 11 Pro
Nova Lima ABC-783 ST: 4P8PXG3 3333668 Sheila Souza sheila.souza@abcdaconstrucao.coom.br CSC SIM WIN 11 Pro
BH - Capacitação ABC-784 ST:F255WF3 Mário Cesário mario.cesario@abcdaconstrucao.com.br Compras sim windowns 11 Pro
LUANA CRISTINA ABC-785
CD - MINAS ABC-786 Emilly Coelho emilly.coelho@abcdaconstrucao.com.br FEP SIM WIN11 PRO
Arquitetura ABC-78 3333668 Lucas Ferreira Assis lucas.assis@abcdaconstrucao.com.br
Fator SI ABC-788
Andréia Ricardo ABC-789 3438836
ABC-790
ABC-791 JPR28J3 Emanuel Oliveira emanuel.oliveira@abcdaconstrucao.com.br Seguraçã do trabalho sim Windowns 11 Pro
CDM - FEP ABC-792 ST: HNR28J3 3438836 Rhayanne Littieri rhayanne.littieri@abcdaconstrucao.com.br FEP Sim Windows 11 pro
MATRIZ - CONTABILIDADE ABC-793 3438836 Cíntia Costa
ABC-794 3438836 Edgard Figueiredo
Thabatha - CAF ABC-795 ST:DRP28J3 Thabata thabatamartins@abcdaconstrucao.com.br CAF SIM WIN10
ABC-796
ABC-797 3438836
Home Office - BH ABC-798 3438836 Sheila Patricia de Souza sheila.souza@abcdaconstrucao.com.br B2B SiM WIN10
C.D.A-Sumaré ABC-799 lucas.felipe lucas.felipe@abcdaconstrucao.com.br C.D.A - Sumaré SIM WIN11
CD - MINAS ABC-800 7PR28J3 Daniel Lobo daniel.lobo@grupomysa.com.br compras Sim Windws 11
CD - MINAS PPP ABC-801 3438836 Thamires Silva thamires.silva@abcdaconstrucao.com.br PPP Sim Windowns 11 Pro
CAF ABC-802 3438836 Lucilene Gomes
Ana Cristina ABC-803 198338
RH ABC-804 BRJ124MHX8 Maria Eduarda Sá mariaeduarda.sa@abcdaconstrucao.com.br Seguraçã do trabalho Sim Windowns 11 Pro
CD - MINAS ABC-805
Marcelo Almeida ABC-806 ST:C159QJ3 Marcelo Almeida marceloalmeida@abcdaconstrucao.com.br Diretoria
Raphael FATOR SI ABC-807 2PR28J3 Thales Souza thales.souza@abcdaconstrucao.com.br TRANSPORTE Sim Windowns 11 Pro
MATRIZ - Capacitação ABC-808 ST:9PR28J3 Marcus Ramos marcus.ramos@abcdaconstrucao.com.br Capacitação Sim Windowns 11 Pro
Matheus Lemos ABC-809
MATRIZ - CONTABILIDADE ABC-810 ST:8PR28J3 Cristiane Loures cristiane.loures@abcdaconstrucao.com.br MATRIZ - CONTABILIDADE SIM WIN10
Expansão ABC-811 Victor Pereira victor.pereira@abcdaconstrucao.com.br
Gilson Peixoto ABC-812
Telefonista ABC-813
Iago Bernardino ABC-814 JNR28J3 Fabio Milanez fabio.milanez@abcdaconstrucao.com.br Dpto De Transporte sim Windowns 11 Pro
CD - MINAS ABC-815 ST: 4LLG4K3 203604 Kleber giovane.agostinho@abcdaconstrucao.com.br TRANSPORTE SIM WIN10 GARANTIA 3 ANOS
CD - MINAS ABC-816 ST: FGBG4K3 203604 Caroline Beluzzo caroline@abcdaconstrucao.com.br Pós Vendas SIM WIN10 GARANTIA 3 ANOS
Nova Lima - MKT ABC-817 ST: DLLG4K3 203604 Laura Rodrigues laura.rodrigues@abcdaconstrucao.com.br compras SIM WIN10 GARANTIA 3 ANOS
CD - MINAS ABC-818 ST: BLLG4K3 203604 Mateus Santinon mateus.santinon@abcdaconstrucao.com.br MEA SIM WIN10 GARANTIA 3 ANOS
CD - MINAS ABC-819 ST: BGBG4K3 203604 Gustavo Tagliati gustavo.tagliati@abcdaconstrucao.com.br MEA SIM WIN10 GARANTIA 3 ANOS
Matriz - Capacitação ABC-820 ST: BMLG4K3 203604 Luana Carvalho luana.carvalho@abcdaconstrucao.com.br Capacitação SIM Windows 11 Pro GARANTIA 3 ANOS
CD - MINAS ABC-821 ST: HMLG4K3 203604 Henrik Visconde henrik.visconde@abcdaconstrucao.com.br Transporte SIM WIN10 GARANTIA 3 ANOS
CD - MINAS ABC-822 ST: 3NLG4K3 203604 Alexandre Borges alexandre.borges@abcdaconstrucao.com.br Operação SIM WIN11 GARANTIA 3 ANOS
CD - MINAS ABC-823 ST: FCBG4K3 203604 Isabela Oliveira isabela.oliveira@abcdaconstrucao.com.br PCE SIM WIN10 GARANTIA 3 ANOS
CD - MINAS ABC-824 ST: 5GBG4K3 203604 Diego Menzonatto diego.gomes@abcdaconstrucao.com.br PCE SIM WIN10 GARANTIA 3 ANOS
CD - MINAS ABC-825 ST: FFBG4K3 203604 Geovanni Silva geovanni.silva@abcdaconstrucao.com.br PCL SIM WIN10 GARANTIA 3 ANOS
CD - MINAS ABC-826 ST: HLLG4K3 203604 Hildmara Teixeira hildmara.gouvea@abcdaconstrucao.com.br PCE SIM WIN10 GARANTIA 3 ANOS
Pós Venda - CDM ABC-827 ST: 1MLG4K3 Aline Tirapani aline.tirapani@abcdaconstrucao.com.br Pós Venda Sim Windowns
CD Minas - Curadoria ABC-828 ST: FLLG4K3 203604 Apredizes Maria Eduarda e Maryane Andreza mariaeduarda.souza@abcdaconstrucao.com.br / maryane.santos@abcdaconstrucao.com.br Compras - Curadoria Sim Windows 11 pro
André Volpato ABC-829 ST: 18T32L3 3711684 André Volpato andre.volpato@abcdaconstrucao.com.br TI - DEV NÃO Ubuntu 23.04.3 LTS GARANTIA 3 ANOS - Senha ( qwe123!@#)
Dir. Juridico ABC-830 ST : 159QJ3 3502044 Hugo Moura Juridico SIM WIN10
Dir. Compras ABC-831 ST: B159QJ3 3502044 Daniel Antoniassi daniel.antoniassi@abcdaconstrucao.com.br Compras
CD - MINAS ABC-832 ST: 7MLG4K3 3502044 Ranieri Vale ranieri.vale@abcdaconstrucao.com.br Segurança Patrimonial SIM WIN10 GARANTIA 3 ANOS
Setor CRM /Growth ABC-833 3502044 Rodrigo Oliveira rodrigo.oliveira@abcdaconstrucao.com.br Growth SIM WIN10 GARANTIA 3 ANOS
CD - MINAS ABC-834 HFBG4K3 3502044 Sara Oliveira sara.oliveira@abcdaconstrucao.com.br MEA sim windowns 11 Pro GARANTIA 3 ANOS
Consultor de Franq. ABC-835 ST: 3564351 Rafael Osava CAF
Gerente de Franquias ABC-836 ST: GFBG4K3 Nathalia santos nathalia.santos@abcdaconstrucao.com.br Q&A Sim Windowns 11 Pro
CDA muriaé ABC-837 ST: 1NLG4K3 203604 Fagner Boalente fagner.boalente@plenalogistica.com.br CDA - Muriaé SIM Windowns 11 Pro GARANTIA 3 ANOS
CDA-MONTES CLAROS ABC-838
Thais Tássia Pereira ABC-839 ST: FLGB1M3 3794108
Home Office ABC-840 ST:3LGB1M3 3794108 Cassiano cassiano.mesquita@abcdaconstrucao.com.br TI - Desenvolvimento Ubuntu 20.04.3 LTS Supp0rt3#01@@
Home Office ABC-841 ST:DXFB1M3 3795274 Ramon Soares ramon.soares@abcdaconstrucao.com.br Expansão sim WIN 10
Home Office ABC-842 ST:BXFB1M3 3795274 Talles talles.gazel@abcdaconstrucao.com.br TI - Desenvolvimento Ubuntu 20.04.3 LTS lNX74@##
CD - MINAS ABC-843 ST: 4XFB1M3 3795274 LEONARDO SILVEIRA leonardo.silveira@abcdaconstrucao.com.br PLANEJ DE CANAIS DIGITAIS SIM WIN10
RH ABC-844 ST:8XFB1M3 3795274 Maura maura.bianca@abcdaconstrucao.com.br RH SIM WIN10
Marketing ABC-845 ST:FXFB1M3 3795274 Natália Garcia natalia.garcia@abcdaconstrucao.com.br Marketing SIM Windows 11 Pro
CD - MINAS ABC-846 ST:5XFB1M3 3795274 Leandro leandro.viana Compras SIM WIN10
Expansão ABC-847 ST:9XFB1M3 3795274 Laura Barretos laura.barreto@abcdaconstrucao.com.br Expansão Sim WIN10
Transporte ABC-848 ST:CXFB1M3 3795274 Aarão Souza aarao.souza@abcdaconstrucao.com.br Transporte SIM Windows 11 Pro
Contabilidade ABC-849 ST:7XFB1M3 3795274 Maria Almeida maria.almeida@abcdaconstrucao.com.br Contabilidade SIM WIN10
ABC-850 ST:6XFB1M3 3795274 sim WIN10
ABC-851 ST:CLGB1M3 3794108 Fabiana Silva fabiana.silva@abcdaconstrucao.com.br Fep Dpto De Faturamento E Expedicao De Pedidos Sim Windows 11 Pro
CD - MINAS ABC-852 ST:2MGB1M3 3795274 Sandra Jesus sandra.jesus@grupomysa.com.br RH sim Windows 11 Pro
ABC-853 ST:8LGB1M3 3794108
CDA-BH ABC-854 TAG:GZ0YYK3 3705217 CDA-BH
CDA-BH ABC-855 TAG:8MX12L3 3705217 CDA-BH
TI - Matriz ABC-856 JKGB1M3 3794108 Fábio Melllo
CD - MINAS ABC-857 2LGB1M3 3794108 Leandro Silva Junior
CD - MINAS ABC-858 ST:6LGB1M3 3794108
CD - MINAS ABC-859 ST:7LGB1M3 3794108
CD - MINAS ABC-860 ST:JLGB1M3 3794108 Diogo Lima diogo.lima@abcdaconstrucao.com.br Fep Dpto De Faturamento E Expedicao De Pedidos Sim Windows 11 Pro
BH - Capacitação ABC-861 ST:9LGB1M3 3794108 Fernanda fernanda.santana@abcdaconstrucao.com.br Capacitação Sim WIN10
Expanção (arquitetura) ABC-862 CKGB1M3 32512 Seteves Rocha steves.rocha@abcdaconstrucao.com.br Sim WIN10 Avell
Central de Espcificação ABC-863 AVNB22030605 32512 Lyandra kayo.armando@abcdaconstrucao.com.br Sim WIN10 Avell
Martiz - Expansão ABC-864 DKGB1M3 3794108 MARIA GOMES GONCALVES maria.gomes@abcdaconstrucao.com.br Expansão WIN10
Gestão de Processos ABC-865 FKGB1M3 3794108 Raissa raissa.guedes@abcdaconstrucao.com.br Sim WIN10
CD - MINAS ABC-866 BLGB1M3 3794108 Fellipe Oliveira fellipe.oliveira@grupomysa.com.br canais digitais Sim Windows 11 Pro
Matriz ABC-867 HKGB1M3 3794108 Camila Campos camila.campos@abcdaconstrucao.com.br DP Sim Windowns 11 Pro Emprestimo
Nova Lima / Consultores ABC-868 1MGB1M3 3794108 Elidiane Fernandes elidiane.fernandes@abcdaconstrucao.com.br Consultora de Franquia Sim Windowns 11 Pro Garantia
Contabilidade ABC-869 HLGB1M3 3794108 Rafael Costa rafael.costa@abcdaconstrucao.com.br Contabilidade Sim WIN10
Manutenção ABC-870 CKGB1M3 3794108 Adilaine Tagliate
Matriz - Expansão ABC-871 DLGB1M3 3794108 Gisele Mendes gisele.mendes@abcdaconstrucao.com.br Expansão Sim Windowns 11 Pro
CD - MINAS ABC-872 GKGB1M3 3794108 Carlos T.I. (SERÁ TROCADO O DESKTOP DO RODRIGO RH)
CD - MINAS ABC-873 5LGB1M3 3794108 Elaine Mello elainedemelo@abcdaconstrucao.com.br Coordenador Logistica
CD - MINAS ABC-874 GLGB1M3 3794108 Marcelo Bruzzi marcelo.bruzzi@abcdaconstrucao.com.br Sim Win10
Matriz - CAF ABC-875 1LGB1M3 3794108 karen Custodio karen.custodio@abcdaconstrucao.com.br CAF Sim Windowns 10 Pro
Outlet ABC-876
Outlet ABC-877
Matriz Contas a Pagar ABC-878 ST:4LGB1M3 3794108 carla.patricia@abcdaconstrucao.com.br Contas a Pagar Sim Windows 11
BI ABC-879 ST:BKGB1M3 vitor.cunha vitor.cunha@abcdaconstrucao.com.br BI Sim WIN10
ABC-880 657800223 Willians Mantovani willians.mantovani@abcdaconstrucao.com.br Growth - Expansão Sim WIN10
Estagio - Expansão ABC-881 ST: BDV6XM3 657800223 Vitoria Melo vitoria.melo@abcdaconstrucao.com.br Expansão Sim Windows 11 Pro
compras CD ABC-882 ST: J7T32L3 Marcela Mendes marcela.mendes@abcdaconstrucao.com.br Compras SIm WINDOWS 11
rafael.cunha ABC-883 rafael.cunha rafael.cunha@abcdaconstrucao.com.br CTE WINDOWS 11
Growth - Nova Lima ABC-884 ST:BFV6XM3 3893889 Yasmin Reis yasmin.reis@abcdaconstrucao.com.br Growth Sim Windows 11 Pro
CONTABILIDADE ABC-885 ST:8CV6XM3 3893889 Yanka Oliveira
ABC-886 ST:3DV6XM3 3893889
Transporte ABC-887 ST:5DV6XM3 3893889 Augusto Pessoa augusto.pessoa@abcdaconstrucao.com.br Transporte Sim Windows 11 Pro Lnx#754
BH - DEV ABC-888 ST:CFV6XM3 3893889 José Luiz jose.souza@abcdaconstrucao.com.br DEV Ubuntu 20.04.3 LTS Lxn888#
BH - DEV ABC-889 ST: HDV6XM3 3893889 Douglas Reis douglas.reis@abcdaconstrucao.com.br DEV Ubuntu 20.04.3 LTS Lxn889#
Martiz - Expansão ABC-890 ST: 7DV6XM3 3893889 Cristiane Silva cristiane.silva@abcdaconstrucao.com.br Consultora de Franquia Sim Windows 10 Pro
BH - DEV ABC-891 ST: FDV6XM3 3893889 Tiago Henrique tiago.henrique@abcdaconstrucao.com.br DEV Ubuntu 20.04.3 LTS Lxn891#
C. Lafaiete ABC-892
CD - MINAS ABC-893 ST: 6DV6XM3 3893889 Vinícius Compras Sim Windows 10 Pro
CD - MINAS ABC-894 ST: 25RZVM3 3878958 leynara neves leynara.neves@abcdaconstrucao.com.br Monitoramento Sim Windows 11 Pro
CD - MINAS ABC-895 ST: 4DV6XM3 3893889 Ecio Chipolesch ecio.chipolesch@abcdaconstrucao.com.br MENOR APRENDIZ (SEG. do Trabalho) Sim Windows 10 Pro Responsável: JADE
ABC-896
CD - MINAS ABC-897 ST: HCV6XM3 3893889 Patrícia Lopes patricia.lopes@abcdaconstrucao.com.br COMPRAS Sim Windows 11
CD - MINAS ABC-898 ST: 6CV6XM3 3893889 Emanuelly Souza emanuelly.souza@abcdaconstrucao.com.br RH Sim Windows 11 Entregue
Matriz ABC-899 ST: J4RZVM3 3878958 Arlindo Bruni arlindo.bruni@abcdaconstrucao.com.br SESMT Sim Windows 11 Pro
CD - MINAS ABC-900 ST: HS4XPM3 3893889 Tiago Branco tiago.branco@abcdaconstrucao.com.br Logística Sim Windows 10
ABC-901 Fábio T.I T.I T.I Ubuntu 20.04.3 LTS Lxn901#
CD - MINAS ABC-902 ST:15RZVM3 3878958 Heverton Silva heverton.silva@abcdaconstrucao.com.br Transporte sim Windows 11
CD - MINAS ABC-903 ST:73RZVM3 3878958 Igor Barroso Frade igor.frade@abcdaconstrucao.com.br Logística Sim Windows 10 Pro
CD - MINAS ABC-904 ST:55RZVM3 3878958 Julio Silva julio.silva@abcdaconstrucao.com.br PCE Sim Windows 11 Pro
CD - MINAS ABC-905 ST:7FV6XM3 3893889 Jaaziel Solas jaaziel.morais@abcdaconstrucao.com.br Transporte
CD -MINAS ABC-906 ST:34ZRZVM3 3878958 Maria Camila camila.evangelista@abcdaconstrucao.com.br Compras
Matriz - Venda Externa ABC-907 ST:HT4XPM3 3878958 Cleidiane Copertino cleidiane.copertino@abcdaconstrucao.com.br PPP sim Windows 11 Pro
Fiscal ABC-908 ST:65RZVM3 3878958 Débora Campos Sim Windows 11 Pro
QUALIDADE E AUDITORIA ABC-909 ST:H4RZVM3 Jóse Vitor Pinehiro da Silva jose.vitor@abcdaconstrucao.com.br Qualidade PCE Sim Windows 11 Solicitação do melhoria de processos, autorizado pelo MA
BH - DEV ABC-910 ST:F4RZVM3 3878958 Leandro Mendes leandro.mendes@abcdaconstrucao.com.br DEV Ubuntu 20.04.3 LTS Lxn910#
RH - Matriz ABC-911 ST:14RZVM3 38778958 Giovana Ferreira giovana.ferreira@abcdaconstrucao.com.br RH Sim Windows 11 pro
T.I - MATRIZ ABC-912 ST:13RVZM3 38778958 IagoRafaelMarquesBer iago.bernardino@abcdaconstrucao.com.br T.I sim Windows 11 Pro
Transporte ABC-913 ST:6S4PXM3 38778958 Yan Gaspar yan.gaspar@abcdaconstrucao.com.br Transporte
CD - MINAS ABC-914 38778958 Maria Macedo maria.macedo@grupomysa.com.br Compras Sim windowns 11 Pro
Escritório Nova Lima ABC-915 ST:8R4XPM3 38778958 André Moreira andre.moreira@abcdaconstrucao.com.br Marketing Sim Windows 10 Pro
Gerente de processos ABC-916 ST:84RZVM3 3878958 Patrcia Maciel SIM
ABC-917 ST:4S4XPM3 3867088 Israel Ismanne israel.ismanne@abcdaconstrucao.com.br R&S sim Windows 11 Pro
PPP ABC-918 ST:GS4PXM3 38778958 Ana Lopes ana.lopes@abcdaconstrucao.com.br PPP Sim
T.I. ABC-919 ST:3Z8F873 FABIO TEOTONIO WIN11 TESTE WIN11
Matriz - Consultor Franquia ABC-920 ST:35RZVM3 304882 Jonathan Camargo jonathas.camargos@abcdaconstrucao.com.br Expansão Franquias
Diretor Ecommerce ABC-921 ST:FXVLYP3 Matheus Lemos matheus.lemos@abcdaconstrucao.com.br Ecommerce Sim W
T.I. - Infra ABC-922 Brian Rodrigues brian.rodrigues@abcdaconstrucao.com.br Infra
Matriz ABC-923 G6LRRN3 4057121 Vitor Guedes vitor.guedes@abcdaconstrucao.com.br Expansão Sim Windows 10 Pro
Segurança do Trabalho - CDM ABC-924 ST:G5RZVM3 3878958 Luciana Ribeiro luciana.ribeiro@abcdaconstrucao.com.br Compras Sim Windows 11 Pro
CD - MINAS ABC-925 Carlos CTE
Gerente Divinopolis ABC-926 ABC Geisilaine Loja
Contas a Pagar ABC-927 ST:GPS7KN3 4057121 Lara Oliveira
Ramon ABC-928 ST:CMS7KN3 4057121 Ramon Jurídico ramon.vilela@abcdaconstrucao.com.br Jurídico Sim Windows 11
Luiz Felipe Albino ABC-929 ST: 66LRRN3 4057121 Luiz Felipe Albino luizfelipe.albino@abcdaconstrucao.com.br growth Sim Windows 11
CD - MINAS ABC-930 ST:7z8f873 Yasmin Cardoso yasmin.cardoso@abcdaconstrucao.com.br Operação Sim Windows 11 Desktop
CD MINAS ABC-931 ST:J5LRRN3 Brian Rodrigues brian.rodrigues@abcdaconstrucao.com.br TI Sim Windows 11 Notebook Dell I5 Novo
Beatriz FATOR SI ABC-932 ST:GTLRRN3 Beatriz Fator beatriz.fatorsi@abcdaconstrucao.com.br FATOR Sim Windows11
Compras ABC-933 ST:7MS7KN3 4057121 Eduardo Frizzero eduardofrizzero@abcdaconstrucao.com.br COMPRAS SIM Windows 11
Vendedor Outlet Av. Brasil ABC-934 Vilmar Saulo saulo@abcdaconstrucao.com.br Vendas Outler Avenida Brasil Sim Windows 10
CAF - Matriz ABC-935 ST: D5LRRN3 4057121 Miguel Junior miguel.junior@abcdaconstrucao.com.br CAF Sim Windows 11
Fiscal ABC-936 ST:87LRRN3 4057121 Gabriella Cugola gabriella.cugola@abcdaconstrucao.com.br Fiscal Sim Windows 10
ABC-937 ST:H7LRRN3 4057121 Roberto Vasconcelos roberto.vasconcelos@abcdaconstrucao.com.br WMS Sim Windows 11 Estagiário
Matriz - Caf ABC-938 ST:GMS7KN3 4057121 Daniel.Costa DanielCosta caf Sim Windows 11
CD - MINAS ABC-939 ST:6MS7KN3 4057121 Walmor walmor Faturamento Sim Windows 11
Transporte ABC-940 ST:HRL55N3 4057121 Marcela de Freitas marcela.santos@abcdaconstrucao.com.br Transporte Sim Windows 11 Entregue
CD - MINAS ABC-941 ST: 2VMRRN3 4057121 Natthan Carlos natthan.carlos@abcdaconstrucao.com.br COMPRAS Sim Windows 11
ABC-942 ST: C5LRRN3 4057121 LAVINIA MENDES CAMPOS lavinia.campos@abcdaconstrucao.com.br Farming Sim Windows 11
Operação ABC-943 ST:B7LRRN3 4057121 Otavio Carpanez otavio.souza@abcdaconstrucao.com.br Marketplace Sim Windows 11
Matriz - ABC-944 ST:BNS7KN3 4057121 Jonathan Arancibia jonathan.arancibia@plenalogistica.com.br Comunicação Interna Sim Windows 11
CD - MINAS ABC-945 4057121 Sidimar Quetz sidimar.quetz@abcdaconstrucao.com.br MEA Sim Windowns 11 Pro ABC@945#
Matriz ABC-946 Diego Pedroso Expansão
Diretoria ABC-947 ST:DZW0LQ3 4234427 Tomas Penna
Matriz ABC-948 38725 Andrezza Arquitetura
Fábio T.I ABC-949 edwilson.diniz@abcdaconstrucao.com.br 3878958 Fabio T.I
cd minas rh ABC-950 ST: DXJVVM3 3878958 Marcela Adum marcela.adum@abcdaconstrucao.com.br S Windows 10 pro
CD - MINAS ABC-951 Lenovo Desktop Rodolfo Souza rodolfo.souza@abcdaconstrucao.com.br Aux Adm -FPP Sim Windows 11
jhosever.ferraz ABC-952 ST: F141LQ3 324816 CDM jhosever.ferraz@abcdaconstrucao.com.br sim WIN 11
CD COMPRAS ABC-953 ST: 2141LQ3 324816 Julia Moreira julia.moreira@abcdaconstrucao.com.br COMPRAS SIM WIN 11 Pediu troca para notebook com tecl. numérico
MATRIZ - Infra ABC-954 ST: D141LQ3 324816 vitor.gruppi vitor.gruppi@abcdaconstrucao.com.br Infra Sim Windows 11
CD - MINAS ABC-955 ST: 8241LQ3 324816 Karoliny Kreppke karoliny.kreppke@grupomysa.com.br PCE Sim Windows 11
ABC-956 ST:HGT6LB3 4266392 Elizandro Santos elizandro.santos@abcdaconstrucao.com.br Desenvolvedor Backend Pleno Ubuntu u8untu##
CD - MINAS ABC-957 ST:B041LQ3 324816 Mariana Carvalho mariana.carvalho@abcdaconstrucao.com.br Ppp Sim Windows 11
CD - MINAS ABC-958 ST: C141LQ3 324816 Leynara Neves leynara.neves@abcdaconstrucao.com.br Monitoramento sim Windowns 11 Pro
CD - MINAS ABC-959 ST: 3241LQ3 324816
CD - MINAS ABC-960 ST: 3241LQ3 4266392 Dagmar Silva dagmar.silva@abcdaconstrucao.com.br POS-VENDAS
CAF - Matriz ABC-961 ST: HCY16Q3 4250275 Vilma Silva vilma.silva@abcdaconstrucao.com.br CAF Sim windows 10 Pro
CD MINAS - GENTE E GESTÃO ABC-962 ST: GCY16Q3 4250275 Danilo Simoso Grasso danilo.grasso@abcdaconstrucao.com.br Gente Gestão Sim Windows 11
CD MINAS - RH ABC-963 ST: 4DY16Q3 4250275 Débora Mattos debora.mattos@abcdaconstrucao.com.br RH Sim Windows 11
CD - MINAS ABC-964 ST: 8CY16Q3 4250275 Kamilly Silva kamilly.Silva@abcdaconstrucao.com.br Transporte Wind 11
CD - MINAS ABC-965 ST: 2FY16Q3 4250275 Vanessa Ramos vanessa.ramos@abcdaconstrucao.com.br Transporte Sim Windows 11 pro
CD - MINAS ABC-966 ST: CQX16Q3 4254325 Rafaely Vitória rafaely.oliveira@abcdaconstrucao.com.br DP Sim Windows 11
CD - MINAS ABC-967 ST: 4FY16Q3 4250275 Igor Brugger igor.brugger@abcdaconstrucao.com.br E-Commercce
CD - MINAS ABC-968 ST: 8FY16Q3 4250275 Ana Beatriz Severino anabeatriz.severino@abcdaconstrucao.com.br Compras sim Windowns 11 Pro
Matriz - Planejamento Estratégico ABC-969 ST: 3FY16Q3 4250275 Fernando Castro fernando.castro@abcdaconstrucao.com.br Growth Sim Windows 11
CD - MINAS ABC-970 ST: CFY16Q3 4250275 Arthur Barone arthur.barone@abcdaconstrucao.com.br Marketing Sim Windows 11
T.I - MATRIZ ABC-971 ST: 3XVTPP3 4137511 Henrique Coimbra DIRETOR VENDAS
Matriz - Canais Digitais ABC-972 ST: GFY16Q3 4250275 Yasmim Souza yasmim.souza@abcdaconstrucao.com.br Canais Digitais Sim Windows 11
MATRIZ - AUDITORIA INTERNA ABC-973 ST: 9FY16Q3 4250275 Alessandra Costa alessandra.costa@abcdaconstrucao.com.br AUDITORIA INTERNA Sim Windows 11
CD - MINAS ABC-974 ST: D041LQ3 324816 Rafael Pimont rafael.pimont@abcdaconstrucao.com.br Gerente de Operações Sim Windows 11
Matriz - CAF ABC-975 PE09F218 70822 Gabriela Silva gabriela.silva@abcdaconstrucao.com.br CAF SIM WIN 11 LENOVO
LENOVO Canais Digitais ABC-976 PE09F20P 70822 Vitor Hugo Oliveira vitorhugo.oliveira@abcdaconstrucao.com.br Canais Digitais SIM Windows 11 Pro LENOVO
Desenvolvedor ABC-977 Diogo Oliveira diogo.oliveira@abcdaconstrucao.com.br TI - Desenvolvedor Sim Ubuntu Lxn977#
Nova Lima - Expansão ABC-978 ST: 2PYXYRR3 4469293 Pedro Oliveira pedro.oliveira@abcdaconstrucao.com.br Expansão Sim Windows 11
Pablo TI ABC-979 ST: 16JBZS3 455217 Pablo T.I
Yasmim Souza matriz ABC-980 ST: J5JBZS3 4552517 Yasmim Souza Yasmim.Souza@abcdaconstrucao.com.br Expansão Sim Windowns 11 Pro
CD MINAS ABC-981 ST:C5JBZS3 4552517 Wesley Miranda wesley.miranda@abcdaconstrucao.com.br mostruário Sim windowns 11 Pro
RH ABC-982 ST: 36JBZS3 4552517 laura lopes laura.lopes@abcdaconstrucao.com.br RH Sim Windowns 11 Pro
Matriz - Gestão ABC-983 ST: H5JBZS3 4552517 Monique Nascimento monique.nascimento@abcdaconstrucao.com.br Gestão Sim Windowns 11 Pro
CD Minas ABC-984 ST: 46JBZS3 4552517 Grasiela Macedo grasiela.macedo@abcdaconstrucao.com.br RH Sim Windowns 11 Pro
Loja Dexco ABC-985 ST: 26JBZS3 4552517 Bianca bianca@abcdaconstrucao.com.br Loja Dexco Sim Windows 11 pro
Loja Dexco ABC-986 ST: D5JBZS3 4552517 Renan Marchesini renan.marchesini@abcdaconstrucao.com.br Loja Dexco Sim Windows 11 pro
Matriz - Capaciatação ABC-987 ST: G5JBZS3 4552517 Laíse Machado laise.machado@abcdaconstrucao.com.br Capacitação Sim Windowns 11 pro
Matriz T.I ABC-988 ST: B5JBZS3 4552517 Matriz T.I rafael.indiani@abcdaconstrucao.com.br Financeiro
CDM - TRANSPORTE ABC-989 ST: F5JBZS3 4552517 Rafaela Moraes rafaela.moraes@abcdaconstrucao.com.br Transporte Sim Windows 11 pro
CD Minas ABC-990 ST: 95JBZS3 4552517 Mariana Gonçalves mariana.goncaleves@abcdaconstrucao.com.br Compras Sim Windows 11 pro
Nova Lima ABC-991 XRV7KGM7ND 30168 Elvis elvis.laurenco@abcdaconstrucao.com.br Marketing MaOs Abc159753
Matriz - Gente e Gestão ABC-992 ST: 8LB0LQ3 4235818 801 lismarque.silva@abcdaconstrucao.com.br Gente e Gestão Sim Windows 11 Pro i7 reserva
Nova Lima ABC-993 PE09Q5WL 336487 Tiago
CD MINAS ABC-994 36618521943 0 Ana Capitulino ana.capitulino@abcdaconstrucao.com.br Sesmt sim Windows 11 Pro Máquina do médico.
Expansão ABC-995 ST:1FZ5JT3 4618708 Leticia Oliveira leticia.oliveira@abcdaconstrucao.com.br Expansão Sim Win 11 Pro
Marketing - Escritório ABC-996 ST:4DZ5JT3 4618708 Raphaela Zanetti raphaela.zanetti@abcdaconstrucao.com.br Contas a Pagar Sim Win 11 Pro
Matriz - Expansão ABC-997 ST:JDZ5JT3 4618708 Guilherme.Santana guilherme.santana@abcdaconstrucao.com.br Expansão Sim Windows 11 Pro
Expansão ABC-998 ST:3DZ5JT3 4618708 Caio Gomes caio.gomes@abcdaconstrucao.com.br Expansão Sim Win 11 Pro
Matriz - Compras ABC-999 ST:9DZ5JT3 4618708 Gabriela Lopes gabriela.lopes@abcdaconstrucao.com.br Compras sim Win 11 Pro
CD Minas ABC-1000 ST:6DZ5JT3 4618708 João Brandao joao.brandao@abcdaconstrucao.com.br MEA Sim Win 11 Pro
CD Minas ABC-1001 ST:BDZ5JT3 4618708 João Hermes joao.ferreira@abcdaconstrucao.com.br Compras Sim Windows 11 Pro
CD Minas ABC-1002 ST:DDZ5JT3 4618708 Isabella Vieira isabella.vieira@abcdaconstrucao.com.br Trasporte sim Win 11 Pro
Matriz - Expansão ABC-1003 ST:JCZ5JT3 4618708 Ramon de Souza Soares ramon.soares@abcdaconstrucao.com.br Expansão Sim Win 11 Pro
Matriz T.I ABC-1004 ST:GDZ5JT3 4618708 Matriz T.I
Matriz T.I ABC-1005 ST:2FZ5JT3 4618708 Matriz T.I
Matriz T.I ABC-1006 ST:HCZ5JT3 4618708 Matriz T.I
CD Minas ABC-1007 ST:1DZ5JT3 4618708 João Martins joao.martins@abcdaconstrucao.com.br Compras sim Win 11 Pro
CDS ABC-1008 ST:2DZ5JT3 4618708 Fabio Macedo fabio.macedo@abcdaconstrucao.com.br Estocagem Sim Win 11 Pro
Matriz - Home Office ABC-1009 ST:7DZ5JT3 4618708 Jackson Ferreira jackson.ferreira@abcdaconstrucao.com.br Expansão Sim Win 11 Pro
Matriz T.I ABC-1010 ST:FDZ5JT3 4618708 Matriz T.I
Matriz Expansão ABC-1011 ST:5DZ5JT3 4618708 Junior Santos juniorsantos@abcdaconstrucao.com.br Expansão Sim Win 11 Pro
Matriz - Gestão ABC-1012 ST:8DZ5JT3 4618708 Gestão gabriel.nogueira@abcdaconstrucao.com.br Gente e Gestão Sim Win 11 Pro
CD Minas - Hibrido ABC-1013 ST:HDZ5JT3 4618708 gustavo.diogo@abcdaconstrucao.com.br Central de Leads Sim Win 11 Pro
CDMINAS - Segurança do Trabalho ABC-1014 ST:CDZ5JT3 4618708 Maria Ibarreto maria.ibarreto@abcdaconstrucao.com.br Mea Administrativo Sim Win 11 Pro
UX Desing ABC-1015 AVNB22490207 46665 Diego Silva diego.silva@abcdaconstrucao.com.br Plataforma Digital Sim Win 11 Pro
Home Office T.I ABC-1016 ST: G2Q17V3 4832396 Rafael T.I rafael@abcdaconstrucao.com.br T.I Sim Win 11 Pro
Matriz.T.I ABC-1017 ST: C3Q17V3 4832396 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1018 ST: 32Q17V3 4832396 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz ABC-1019 ST: F2Q17V3 4832396 Thaís Silva thais.silva@plenalogistica.com.br Transporte Sim Win 11 Pro
Nova Lima - Home Office ABC-1020 ST: 73Q17V3 4832396 Caio Fava caio.fava@abcdaconstrucao.com.br T.iI - Desenvolvimento Sim Ubuntu user abc1020
Matriz.T.I ABC-1021 ST: F3Q17V3 4832396 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1022 ST: 53Q17V3 4832396 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1023 ST: 93Q17V3 4832396 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1024 ST: 24Q17V3 4832396 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
CSC ABC-1025 ST: 14Q17V3 4832396 Isabelly Evangelista isabelly.evangelista@abcdaconstrucao.com.br CSC Sim Win 11 Pro
Matriz.T.I ABC-1026 ST: H3Q17V3 4832396 Wallace - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1027 ST: G3Q17V3 4832396 Wallace - Matriz.T.I Matriz.T.I Sim Win 11 Pro
CD-Minas ABC-1028 ST: B3Q17V3 4832396 Karina Costa karina.costa@abcdaconstrucao.com.br Compras Sim Win 11 Pro
Matriz.T.I ABC-1029 ST: 83Q17V3 4832396 Wallace - Matriz.T.I Matriz.T.I Sim Win 11 Pro
CAF - Matriz ABC-1030 ST: 72Q17V3 4832396 Arthur Rodrigues CAF arthur.rodrigues@abcdaconstrucao.com.br CAF Sim Win 11 Pro
Matriz.T.I ABC-1031 ST: 92Q17V3 4832396 Wallace - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz - Expansão ABC-1032 ST: 63Q17V3 4832396 Lucas Honorato lucas.honorato@abcdaconstrucao.com.br Expansão Sim Win 11 Pro
Matriz.T.I ABC-1033 ST: 23Q17V3 4832396 Wallace - Matriz.T.I Maria Alice CSC Sim Win 11 Pro
Matriz.T.I ABC-1034 ST: D3Q17V3 4832396 Wallace - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Home Office ABC-1035 ST: 43Q17V3 4832396 Raphaella Souza raphaella.souza@abcdaconstrucao.com.br PPP Sim Win 11 Pro
TI- Home Office ABC-1036 ST: B2Q17V3 4832396 Luiz Junior - Home Office luiz.junior@abcdaconstrucao.com.br TI Sim Ubuntu 20.04.3 LTS Senha: Lxn#1036
Matriz.T.I ABC-1037 ST: 62Q17V3 4832396 Lucas Lopes lucas.lopes@abcdaconstrucao.com.br Compras Sim Win 11 Pro
Matriz.T.I ABC-1038 ST: C2Q17V3 4832396 Fábio Mello - Matriz Sim Win 11 Pro
Matriz.T.I ABC-1039 ST: 33Q17V3 4832396 Fábio Mello - Matriz Sim Win 11 Pro
CD-Minas ABC-1040 ST: 13Q17V3 4832396 Sara Faier sara.faier@abcdaconstrucao.com.br Transporte Sim Win 11 Pro
Marketing - Home Office ABC-1041 ST: J2Q17V3 4832396 Marcelo Souza marcelo.souza@abcdaconstrucao.com.br Marketing Sim Win 11 Pro
CD Nova Lima ABC-1042 ST: D2Q17V3 4832396 Francielle Batista francielle.batista@abcdaconstrucao.com.br Transporte Sim Win 11 Pro
Matriz.T.I ABC-1043 ST: J3Q17V3 4832396 Fábio Mello - Matriz Sim Win 11 Pro
Matriz.T.I ABC-1044 ST: 82Q17V3 4832396 Fábio Mello - Matriz Sim Win 11 Pro
Matriz.T.I ABC-1045 ST: H2Q17V3 4832396 Nathália Santos nathalia.santos@abcdaconstrucao.com.br qualidade Sim Win 11 Pro
Loja Catalão ABC-1046 ST: 39P46Q3 4231059 Loja Catalão Sim Win 11 Pro
Loja Catalão ABC-1047 ST: JCP46Q3 4231059 Loja Catalão Sim Win 11 Pro
CDA - Cariacica ABC-1048 ST:DZ0YYK3 CDA - Cariacica linnyker.xavier@abcdaconstrucao.com.br CDA - Cariacica Sim Win 10
Matriz - Gestão ABC-1049 ST:3N6PXW3 5083863 Pedro Brito pedro.brito@abcdaconstrucao.com.br Gente e Gestão Sim Win 11 Pro
Matriz.T.I ABC-1050 ST:8N6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Dev - Nova Lima ABC-1051 ST:4N6PXW3 5083863 Robson Oliveira robson.oliveira@abcdaconstrucao.com.br T.I nao Ubuntu 20.04.3 LTS Senha: ABC@18194590
Matriz.T.I ABC-1052 ST:DN6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz. Juridico ABC-1053 ST:6N6PXW3 5083863 Lubya Alvez lubya.alves@abcdaconstrucao.com.br Juridico Sim Win 11 Pro
Matriz.T.I ABC-1054 ST:1N6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1055 ST:JN6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1056 ST:CN6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz - CAF ABC-1057 ST:5N6PXW3 5083863 ryan.carvalho@grupomysa.com.br ryan.carvalho@grupomysa.com.br CAF Sim Win 11 Pro
Matriz.T.I ABC-1058 ST:JM6PXW3 5083863 Daniel Castro daniel.castro@abcdaconstrucao.com.br Compras Sim Win 11 Pro
Capacitação ABC-1059 ST:HM6PXW3 5083863 Teresa Zoet teresa.zoet@abcdaconstrucao.com.br Capacitação Sim Win 11 Pro
Matriz.T.I ABC-1060 ST:HN6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1061 ST:9N6PX23 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1062 ST:7N6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
CD Minas ABC-1063 ST:GM6PXW3 5083863 Carlos Almeida carlos.almeida@abcdaconstrucao.com.br Ti Sim Win 11 Pro
Escritorio Nova Lima - Growth ABC-1064 ST:GN6PXW3 5083863 Marcos Souza marcos.souza@abcdaconstrucao.com.br Growth Sim Win 11 Pro
CD Minas ABC-1065 ST:FN6PXW3 5083863 Elaine de Melo elainedemelo@abcdaconstrucao.com.br Logistica Sim Win 11 Pro
Matriz.T.I ABC-1066 ST:BN6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1067 ST:FM6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
Matriz.T.I ABC-1068 ST:2N6PXW3 5083863 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
CD Minas ABC-1069 ST:3CP46Q3 4231059 Erick Souza - CD Minas T.I Matriz.T.I CDA Sumaré SP Sim Win 11 Pro
Matriz.T.I ABC-1070 ST:1C3F0X3 824068269 Mariana Borsato mariana.borsato@abcdaconstrucao.com.br Marketing Sim Win 11 Pro
Matriz.T.I ABC-1071 PE0AFHDD 84365 Laura Esteves lauraesteves@abcdaconstrucao.com.br Compras Sim windows 11 Pro
Matriz.T.I ABC-1072 PE0AKKQS 84365 Marcos Vaz - Matriz.T.I Matriz.T.I Sim Win 11 Pro
ABC-1073 ST:HBP46Q3 4231059 CDA
Matriz.T.I ABC-1074 2305 Marcos Vaz - Matriz.T.I Matriz.T.I Ubuntu 20.04.3 LTS
Matriz.T.I ABC-1075 2305 Marcos Vaz - Matriz.T.I Matriz.T.I Ubuntu 20.04.3 LTS
Matriz.T.I ABC-1076 2305 Marcos Vaz - Matriz.T.I Matriz.T.I Ubuntu 20.04.3 LTS
Expansão - Matriz ABC-1077 PE09EFTP 369596 Carolina Leitão carolina.leitao@abcdaconstrucao.com.br Expansão Sim Windows 11 Pro
Matriz. T.I ABC-1078 PE09EFYD 369596 Pedro Lima T.I pedro.lima@abcdaconstrucao.com.br TI Win 11 Pro
Nova Lima - DEV ABC-1079 369596 Tiago Fick tiago.fick@abcdaconstrucao.com.br DEV - TI Sim Win 11 Pro
MATRIZ-Expansão ABC-1080 PE09EFV8 369596 Carla Martins Carla Martins Expansão. sim Win 11 Pro
Matriz. T.I ABC-1081 PE09EFYR 369596 Marcos Vaz - Matriz.T.I Matriz.T.I Win 11 Pro
Matriz. T.I ABC-1082 PE09EFYM 369596 edgard figueiredo edgard.figueiredo@abcdaconstrucao.com.br Win 11 Pro
Matriz. T.I ABC-1083 PE09EFYB 369596 Marcos Vaz - Matriz.T.I Matriz.T.I Win 11 Pro
Matriz. T.I ABC-1084 PE09EFV0 369596 Daniel Lisboa daniel.lisboa@plenalogistica.com.br Plena sim Win 11 Pro
Matriz. T.I ABC-1085 PE09EFTW 369596 Marcos Vaz - Matriz.T.I Matriz.T.I Win 11 Pro
Matriz. T.I ABC-1086 PE09EFYZ 369596 Marcos Vaz - Matriz.T.I Matriz.T.I Win 11 Pro
Matriz.T.I ABC-1087 665RB93 369596 CARLOS.PEREIRA Gabriel Sim Win 10 Pro
Matriz - Marketing ABC-1088 9W787Y3 5333021 gustavo.fonseca gustavo.fonseca@abcdaconstrucao.com.br Marketing Sim Windows 11 Pro
Nova Lima - Capacitação ABC-1089 8W787Y3 5333021 Priscila Marcelino priscila.marcelino@abcdaconstrucao.com.br Capacitação Sim Windows 11 Pro
CD Minas - MEA ABC-1090 PE2107 375481 Mateus Santinon mateus.santinon@abcdaconstrucao.com.br MEA Sim Windows 11 Pro
Matriz - Expansão ABC-1091 BNB8WY3 264647 Roberta Carvalho roberta.carvalho@abcdaconstrucao.com.br Expansão Sim Windows 11 Pro
CD Minas - Compras ABC-1092 6MD8WY3 264647 Laura Esteves laura.esteves@abcdaconstrucao.com.br Compras Sim Windows 11 Pro
FEP - CD Minas ABC-1093 3NB8WY3 264647 Nayara Tarciano nayara.tarciano@abcdaconstrucao.com.br FEP Sim Windows 11 Pro
Matriz. T.I ABC-1094 1NB8WY3 264647 Carlos Pereira - Matriz.T.I Sim Windows 11 Pro
Matriz. T.I ABC-1095 HPB8WY3 264647 Carlos Pereira - Matriz.T.I Sim Windows 11 Pro
Matriz. T.I ABC-1096 HNB8WY3 264647 Carlos Pereira - Matriz.T.I Sim Windows 11 Pro
Matriz. T.I ABC-1097 FNB8WY3 264647 Carlos Pereira - Matriz.T.I Sim Windows 11 Pro
Matriz. T.I ABC-1098 2NB8WY3 264647 Carlos Pereira - Matriz.T.I Sim Windows 11 Pro
Matriz. T.I ABC-1099 5NB8WY3 264647 Gabriel Macedo gabriel.macedo@abcdaconstrucao.com.br Sim Windows 11 Pro
Matriz. T.I ABC-1100 6NB8WY3 264647 Bruno Meirelles bruno.meirelles@abcdaconstrucao.com.br Transporte Sim Windows 11 Pro
Matriz. T.I ABC-1101 PE0AJZRQ 90446 Carlos Pereira - Matriz.T.I Sim Windows 11 Pro
Matriz. T.I ABC-1102 BW 9RBZ3 5619430 Wanderlei Silva wanderlei.silva@abcdaconstrucao.com.br T.I sim windows 11 Pro
Matriz. T.I ABC-1103 9W9RBZ3 5619430 Carlos Pereira - Matriz.T.I T.I sim windows 11 Pro
Nova Lima Growth ABC-1104 HW9RBZ3 5619430 Marcos Souza marcos.souza@abcdaconstrucao.com.br Growth sim windows 11 Pro
CAF-matriz ABC-1105 JW9RBZ3 5619430 Sthennyum Santos sthennyum.santos@abcdaconstrucao.com.br CAF Consultores sim windows 11 Pro
Matriz T.I ABC-1106 1X9EBZ3 5619430 Carlos Pereira - Matriz.T.I T.I sim windows 11 Pro
CD Minas ABC-1107 FW9RBZ3 5619430 Josiane Oliveira josiane.oliveira@abcdaconstrucao.com.br Qualidade e Auditoria sim windows 11 Pro
Matriz T.I ABC-1108 GW9RBZ3 5619430 Carlos Pereira - Matriz.T.I T.I sim windows 11 Pro
CD Minas - Faturamento ABC-1109 DW9RBZ3 5619430 Alan Jorge Feliz Fernandes alanfernandes@abcdaconstrucao.com.br Faturamento sim windows 11 Pro
CDM ABC-1110 R9XW508PWWK 18755921 tablet SM-t225 Android 13 IMEI:350538866960547
CDM ABC-1111 R9XW508PS1K 18755921 tablet SM-t225 Android 13 IMEI:350538866959575
CDM ABC-1112 CW9RBZ3 5619430 MEA SIM windows 11 Pro
Matriz T.I ABC -1113 2X9RBZ3 5619430 T.I SIM windows 11 Peo
Matriz I.I ABC-1114 9B7KF82 5837090 Carlos Pereira - Matriz T.I T.I Sim Windows 11 Note que era do Fred
Matriz ABC-1115 080779QBK2015282 5837090 Fabio Teotonio T.I Ubuntu 18 NP300E5L-KF1BR - SAMSUNG
CD Minas ABc-1116 8DSJG04 5837090 Lucas Cruz lucas.cruz@abcdaconstrucao.com.br Compras SIM Windows 11Pro
Matriz - capacitação ABC-1117 3DSJG04 5837090 Raphaela Pires sarah.dutra@abcdaconstrucao.com.br capacitação SIM WINDOWS11
CD Minas ABC-1118 FDSJG04 5837090 Alan Rigolon alan.rigolon@abcdaconstrucao.com.br Compras SIM windows 11 Pro
Matriz ABC-1119 DDSJG04 5837090 CARLOS.PEREIRA T.I SIM windows 11 Pro
Matriz ABC-1120 7DSJG04 5837090 CARLOS.PEREIRA T.I SIM windows 11 Pro
CD Minas - DP ABC-1121 6FSJG04 5837090 Kleyverson Jesus kleyverson.jesus@abcdaconstrucao.com.br RH SIM windows 11 Pro
Nova Lima- CAF Consultor ABC-1122 HDSJG04 5837090 Paola Reis paola.reis@abcdaconstrucao.com.br PPP SIM windows 11 Pro
CD Minas - Melhoria Continua ABC-1123 6DSJG04 5837090 Rafaela Moraes rafaela.moraes@abcdaconstrucao.com.br Melhoria Continua SIM windows 11 Pro
CD Minas ABC-1124 5FSJG04 5837090 Nely Silva nely.silva@abcdaconstrucao.com.br PCL SIM windows 11 Pro
Matriz ABC-1125 5DSJG04 5837090 Marina.Sodré marina.sodre@abcdaconstrucao.com.br T.I SIM windows 11 Pro
CDM ABC-1126 BDSJG04 5837090 Vitoria Cesar vitoria.cesar@abcdaconstrucao.com.br MEA - Administrativo SIM windows 11 Pro
Matriz ABC-1127 2FSJG04 5837090 Jacqueline Jacqueline.campos@abcdaconstrucao.com.br T.I SIM windows 11 Pro
Matriz ABC-1128 4FSJG04 5837090 CARLOS.PEREIRA T.I SIM windows 11 Pro
Nova Lima - Power BI ABC-1129 GDSJG04 5837090 Antônio Gomes antonio.gomes@abcdaconstrucao.com.br Power BI SIM windows 11 Pro
Matriz - Auditoria ABC-1130 3FSLG04 5837090 Priscila Alvares priscila.alvares@abcdaconstrucao.com.br Qualidade SIM windows 11 Pro
CDM ABC-1131 JDSJG04 5837090 Pedro Barros pedro.barros@abcdaconstrucao.com.br melhoria continua SIM windows 11 Pro
Matriz ABC-1132 1FSJG04 5837090 CARLOS.PEREIRA T.I SIM windows 11 Pro
Nova Lima- CAF Consultor ABC-1133 9DSJG04 5837090 Débora Sena debora.sena@abcdaconstrucao.com.br CAF Consultores SIM windows 11 Pro
Nova Lima- Expansão ABC-1134 CDSJG04 5837090 Leandro Pereira leandro.pereira@abcdaconstrucao.com.br Expansão SIM windows 11 Pro
Hibrido - TI ABC-1135 74DSJG04 5837090 Paulo Junior paulo.junior@abcdaconstrucao.com.br T.I SIM windows 11 Pro
Nova Lima - Juridico ABC-1136 9XTG014 5988880 Hugo Mendonça hugomendonca@abcdaconstrucao.com.br Juridico SIM windows 11 Pro
Catalão ABC-1137 B86Q214 372631660 carlos.pereira Catalão T.I SIM windows 11 Pro
Catalão ABC-1138 686Q214 372631660 carlos.pereira Catalão T.I SIM windows 11 Pro
Catalão ABC-1139 786Q214 372631660 carlos.pereira Catalão T.I SIM windows 11 Pro
Catalão ABC-1140 986Q214 372631660 carlos.pereira Catalão T.I SIM windows 11 Pro
Catalão ABC-1141 886Q214 372631660 carlos.pereira Catalão T.I SIM windows 11 Pro
Nova Lima - P.O Produtos ABC-1142 FVFKL0W81WFV 44996 Marcelo Bruzzi marcelo.bruzzi@abcdaconstrucao.com.br TI - P.O Produtos Não MacOS Sonoma Mac Book Air | Login.: marcelo.bruzzi Senha.: ABC#1142@ ou Login: ABC1142 Senha.: TDQ3TpySK6
Home Office - Marketing ABC-1143 FVFKL2WG1WFV 44996 André Rocha andre.rocha@abcdaconstrucao.com.br Marketing Não MacOS Sonoma Mac Book Air | Login.: andre.rocha Senha.: ABC#1143@ ou Login: ABC1142 Senha.: TDQ3TpySK6
Nova Lima - DEV ABC-1144 1YYGH24 6326351 Alan Rodrigues alan.rodrigues@abcdaconstrucao.com.br T.I - Product Owner Sim Windows 11 Pro
Matriz - Power Bi ABC-1145 3YYGH24 6326351 Victor Andrade victor.andrade@abcdaconstrucao.com.br Power Bi Sim Windows 11 pro
ABC-1146 5YYGH24 6326351
Nova Lima - Produto ABC-1147 GXYGH24 6326351 Davi Moreno davi.moreno@abcdaconstrucao.com.br Produto sim Windows 11 pro
Breno.Azevedo - gestao ABC-1148 FXYGH24 6326351 Breno.Azevedo breno.azevedo@abcdaconstrucao.com.br Gestao Sim Windows 11 pro
T.I ERP ABC-1149 JXYGH24 6326351 Tiago olimpio tiago.olimpio@abcdaconstrucao.com.br ERP Sim Windows 11Pro
Nova Lima - Power BI ABC-1150 HXYGH24 6326351 Adinam Gonçalvesadinam.goncalves@abcdaconstrucao.com.br Power BI Sim Windows 11 Pro
ABC-1151 4YYGH24 6326351
ABC-1152 2YYGH24 6326351
ABC-1153 DXYGH24 6326351
Nova Lima - Squad Core Services ABC-1154 RW3C499WFD 46016 edwilson.diniz@abcdaconstrucao.com.br TI Sim MacOS Sonoma Mac Book Air | Login.: edwilson.diniz Senha.: ABC#1154@ ou Login: ABC-1154 Senha.: TDQ3TpySK6
Nova Lima - Team Leader ABC-1155 Y3J9JHC2DX 46016 tiago.henrique@abcdaconstrucao.com.br TI Sim MacOS Sonoma Mac Book Air | Login.: tiago.henrique Senha.: ABC#1155@ ou Login: ABC-1155 Senha.: TDQ3TpySK6
ABC-1156 63RZVM3
T.I infra ABC-1157 MRMOITJ412LXP05 infraT.I fabioandrade@abcdaconstrucao.com.br T.I Não linux Ubuntu
Catão BH ABC-1158 PE0CZPEM 10680 Camila Lobo camila.lobo@abcdaconstrucao.com.br Lojas Proprias Sim Windows 11 Pro
Matriz ABC-1159 PE0CZPEL 10680 Rodrigo José rodrigo.jose@abcdaconstrucao.com.br CRM Sim Windows 11 Pro
CD Minas ABC-1160 PE0CZMX5 10680 Guilherme Braga guilherme.braga@abcdaconstrucao.com.br Compras Sim Windows 11 Pro
Home Office ABC-1161 PE0CZPE9 10680 Nathalie Baptista nathalie.baptista@abcdaconstrucao.com.br E-commerce Sim windows 11 Pro
ABC-1162 PE0CZPED
ABC-1163 PE0CZPEH
ABC-1164 PE0CZPEJ
Vânia de Paula - Fiscal ABC-1165 PE0CZPEK 10680 Fiscal vania.paula@abcdaconstrucao.com.br Fiscal sim windows 11 Pro
ABC-1166 PE0CZMX2
Danilo Grasso - Gestao ABC-1167 PE0CZMX4 10680 Gestão danilo.grasso@abcdaconstrucao.com.br Gestão sim windows 11 Pro
CD Minas ABC-1168 PE0CZPEC 10680 Guilherme Perez guilherme.perez@abcdaconstrucao.com.br Logistica Sim Windonws 11 Pro
T.I infra ABC-1169 PE0CZPE6 10680 carlos.almeida carlos.almeida@abcdaconstrucao.com.br T.I sim Windows 11 Pro
Matriz ABC-1170 PE0CZPEE 10680 Gisely Costa gisely.costa@abcdaconstrucao.com.br Capacitação Sim windows 11 Pro
Matriz- Financeiro ABC-1171 PE0CZPE8 10680 Thays Nascimento thays.nascimento@grupomysa.com.br Financeiro Sim Windows 11 Pro
Matriz ABC-1172 PE0CZPEG 10680 Gustavo Gayer gustavo.gayer@abcdaconstrucao.com.br Marketplace Sim Windows 11 Pro
Loja Propria (Catalão) ABC-1173 PE0CZPE5 10680 Julio Santos julio.santos@abcdaconstrucao.com.br Vendas- Loja Propria Sim windows 11 Pro PC localizado na butique
CD Minas ABC-1174 PE0CZPEF 10680 Ednaldo Carvalho ednaldo.carvalho@abcdaconstrucao.com.br Compras Sim windows 11 Pro
Reginaldo Siqueira Juridico ABC-1175 PE0CZMX1 10680 Reginaldo Siqueira reginaldo.siqueira@abcdaconstrucao.com.br juridico sim Windows 11 Pro
ABC-1176 PE0CZPEN
Nova lima ABC-1177 PE0CZPE7 10680 Gabriel Temponi Gabriel.temponi@abcdaconstrucao.com.br Marketing Sim Windows 11 Pro
Nova Lima ABC-1178 PE0CZPEA 10680 Matheus Lemos matheus.lemos@abcdaconstrucao.com.br Tech & Growth
Matriz ABC-1179 PE0CZPEB 10680 Francisco Piuma francisco.piuma@abcdaconstruca.com.br Ecommerce Sim Windows 11 Pro
CD Minas ABC-1180 PE0CZPEK 11438 Alan Rigolon alan.rigolon@abcdaconstrucao.com.br Compras Sim Windows 11 Pro
Matriz - Gestão de projetos ABC-1181 PE0E5BNL 30172 Felipe.Reis felipe.reis@abcdaconstrucao.com.br Gestão de projetos sim Windows 11 Pro
ABC-1182 PE0E5BN6 30172 Windows 11 Pro
ABC-1183 PE0E5BNM 30172 Windows 11 Pro
Matriz - Expansão ABC-1184 PE0E5BMF 30172 Laura Medeiros laura.medeiros@abcdaconstrucao.com.br Windows 11 Pro
Matriz - Gestão de projetos ABC-1185 PE0E5BG5 30172 Isabela Martiniano isabela.martiniano@abcdaconstrucao.com.br Gestão sim Windows 11 Pro
ABC-1186 PE0DW6KE 30172 sim Windows 11 Pro
Matriz - Expansão ABC-1187 PE0E5BH4 30172 Samara Castro samara.castro@abcdaconstrucao.com.br sim Windows 11 Pro
Matriz - Expansão ABC-1188 PE0E5BGG 30172 Pablo Correa pablo.correa@abcdaconstrucao.com.br sim Windows 11 Pro
Matriz - Expansão ABC-1189 PE0E5BNC 30172 Matheus Pereira matheus.pereira@abcdaconstrucao.com.br sim Windows 11 Pro
Matriz - Expansão ABC-1190 PE0E5BNA 30172 Ana Paula anapaula.vieira@abcdaconstrucao.com.br sim Windows 11 Pro
Matriz - Expansão ABC-1191 PE0E5BG8 30172 Gisele Mendes gisele.mendes@abcdaconstrucao.com.br sim Windows 11 Pro
Matriz - Expansão ABC-1192 PE0E5BGA 30172 Carla Martins carla.martins@abcdaconstrucao.com.br sim Windows 11 Pro
ABC-1193 PE0E5BNJ 30172 sim Windows 11 Pro
ABC-1194 PE0DW6LV 30172 sim Windows 11 Pro
ABC-1195 PE0E5BFX 30172 sim Windows 11 Pro
Matriz - Gestão ABC-1196 PE0E5BND 30172 Monique Nascimento monique.nascimento@abcdaconstrucao.com.br sim Windows 11 Pro
Matriz - Expansão ABC-1197 PE0DW6LL 30172 Matheus Nascimento mateus.nascimento@abcdaconstrucao.com.br sim Windows 11 Pro
Matriz - Expansão ABC-1198 PE0E5BN3 30172 Fabio Almeida fabio.almeida@abcdaconstrucao.com.br sim Windows 11 Pro
Matriz - Expansão ABC-1199 PE0E5BGJ 30172 Luan Rezende luan.rezende@abcdaconstrucao.com.br sim Windows 11 Pro
Matriz - Gestão ABC-1200 PE0E5BN4 30172 Geizianne Ribeiro geizianne.ribeiro@abcdaconstrucao.com.br sim Windows 11 Pro
ABC-1201 PE0E5BTQ 30172 sim Windows 11 Pro
ABC-1202 PE0DW6L3 30172 sim Windows 11 Pro
ABC-1203 PE0E5BGZ 30172 sim Windows 11 Pro
Mariz - T.I ABC-1204 carlos.pereira carlos.pereira@abcdaconstrucao.com.br T.I Infra Nao Linux Mini PC
ABC-1205 sim Windows 11 Pro
ABC-1206 sim Windows 11 Pro
ABC-1207 sim Windows 11 Pro
"""

def sanitize_text(text):
    if not text:
        return None
    # Remove senhas e informações sensíveis
    password_patterns = [
        r'Senha\s*[:.]\s*[\w@#$!%*?&]+', r'abc@\d+#', r'Lxn\d+#',
        r'Supp0rt3#01@@', r'lNX74@##', r'qwe123!@#', r'u8untu##'
    ]
    for pattern in password_patterns:
        text = re.sub(pattern, '[REMOVIDO]', text, flags=re.IGNORECASE)
    # Limpa espaços e caracteres especiais extras
    text = ' '.join(text.split())
    text = text.replace('"', '').replace("'", "")
    return text.strip() if text else None

def parse_data(data):
    records = []
    lines = data.strip().split('\n')

    setores_conhecidos = [
        "loja", "franquia", "vendas", "caixa", "rh", "ti", "monitoramento", "pce", "compra",
        "almoxarifado", "contabilidade", "growth", "caf", "auditoria", "transporte", "mea",
        "csc", "financeiro", "jurídico", "dpto de transporte", "fator-si", "tesouraria",
        "expedição", "gerencia", "fep", "pós vendas", "compras", "diretoria", "dev",
        "fator si", "qualidade", "marketplace", "desenvolvimento", "segurança patrimonial",
        "expansão", "dp", "logistica", "marketing", "fiscal", "juridico", "infra"
    ]

    for line in lines:
        original_line = line
        record = {
            "localizacao": None, "identificador": None, "serial_number": None,
            "usuario": None, "email": None, "setor": None, "ativo": None,
            "sistema_operacional": None, "observacoes": None
        }

        # 1. Extrair Identificador
        id_match = re.search(r'\b(ABC-?\d+(-NB)?)\b', line, re.IGNORECASE)
        if not id_match:
            continue
        record["identificador"] = id_match.group(1).upper()
        record["localizacao"] = line[:id_match.start()].strip() or None
        remaining_line = line[id_match.end():].strip()

        # 2. Extrair e remover padrões específicos
        email_match = re.search(r'[\w\.\-]+@[\w\.\-]+', remaining_line, re.IGNORECASE)
        if email_match:
            record["email"] = email_match.group(0)
            remaining_line = remaining_line.replace(email_match.group(0), "").strip()

        os_pattern = r'\b(Windows[\s\d\w\.\-]*|WIN[\s\d\w\.]*|Ubuntu[\s\d\w\.]*|MacOS[\s\d\w\.]*|Android[\s\d\w\.]*)\b'
        os_match = re.search(os_pattern, remaining_line, re.IGNORECASE)
        if os_match:
            record["sistema_operacional"] = os_match.group(0).strip()
            remaining_line = remaining_line.replace(os_match.group(0), "").strip()

        sn_pattern = r'\b(ST:[\w-]+|PE[\w]+|BRJ[\w]+|[\w]{7,})\b'
        sn_match = re.search(sn_pattern, remaining_line)
        if sn_match and len(sn_match.group(1)) > 5:
            record["serial_number"] = sn_match.group(1)
            remaining_line = remaining_line.replace(sn_match.group(1), "").strip()

        ativo_match = re.search(r'\b(SIM|S|NÃO|N)\b', remaining_line, re.IGNORECASE)
        if ativo_match:
            record["ativo"] = ativo_match.group(0).upper()
            remaining_line = remaining_line.replace(ativo_match.group(0), "").strip()

        # 3. Tentar identificar setor e usuário do restante
        words = [w for w in remaining_line.split() if w]
        possible_user = []
        possible_setor = []
        other_info = []

        for word in words:
            if word.lower() in setores_conhecidos:
                possible_setor.append(word)
            elif re.match(r'^[A-Z][a-z]+$', word):
                possible_user.append(word)
            else:
                other_info.append(word)

        if possible_user:
            record["usuario"] = " ".join(possible_user)
        if possible_setor:
            record["setor"] = " ".join(possible_setor)

        record["observacoes"] = " ".join(other_info) if other_info else None

        # 4. Sanitizar todos os campos de texto
        for key, value in record.items():
            if isinstance(value, str):
                record[key] = sanitize_text(value)

        records.append(record)
    return records

def create_sql_file(records, filename="inventario.sql"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("CREATE TABLE IF NOT EXISTS inventario_computadores (\n")
        f.write("    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    localizacao TEXT,\n")
        f.write("    identificador TEXT,\n    serial_number TEXT,\n    usuario TEXT,\n")
        f.write("    email TEXT,\n    setor TEXT,\n    ativo TEXT,\n")
        f.write("    sistema_operacional TEXT,\n    observacoes TEXT\n);\n\n")

        for record in records:
            valid_keys = [k for k, v in record.items() if v is not None]
            columns = ', '.join(valid_keys)
            values = ', '.join(f"'{str(record[k]).replace("'", "''")}'" for k in valid_keys)
            if columns:
                f.write(f"INSERT INTO inventario_computadores ({columns}) VALUES ({values});\n")

if __name__ == "__main__":
    parsed_records = parse_data(raw_data)
    create_sql_file(parsed_records)
    print(f"Arquivo 'inventario.sql' criado com sucesso com {len(parsed_records)} registros.")
