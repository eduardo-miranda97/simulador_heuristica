# -*- coding:utf-8 -*-


from random import randint
from numpy import random
from copy import deepcopy
from tkinter import Frame
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import datetime
import time

class Simulator(object):

    MAX_ITERATIONS = 200

    def __init__(self, structure_map, wall_map, static_map, crowd_map, dinamic_map, individuals, directory):

        self.structure_map = structure_map
        self.wall_map = wall_map
        self.static_map = static_map
        self.crowd_map = crowd_map
        self.dinamic_map = dinamic_map
        self.individuals = individuals
        self.directory = directory # *********************************************
        self.iteration = 0
        # self.log = Log() ********************
    

    def simulate(self):
        while (not self.check_evacuated_individuals() and self.iteration < self.MAX_ITERATIONS):
            print(self.iteration)
            #self.crowd_map.draw_map("../output/" + self.directory, self.individuals, self.iteration)
            self.crowd_map.draw_map(self.directory, self.iteration)
            self.dinamic_map.draw_map(self.directory, self.iteration)
            self.iteration += 1

            self.sort_individuals_by_distance()

            for individual in self.individuals:
                # Increment the amount of steps for the individual to move based in individual's speed
                individual.steps += 1 
                if (not individual.evacuated):
                    if (individual.steps == individual.speed):

                        direction = individual.move(self.structure_map, self.wall_map, self.static_map, self.crowd_map, self.dinamic_map)
                        # Increase the dinamic map if someone move to the direction
                        if direction:
                            self.dinamic_map.map[direction['row']][direction['col']] += 1

                        if(self.structure_map.isSaida(individual.row, individual.col)):
                            individual.evacuated = True

                        individual.steps = 0

            # After moving all the individuals free the exit gates that are occupied
            self.crowd_map.free_exit_gates()

            # After the iteration it's recalculed the pheromone map
            self.dinamic_map.difusion_decay()

        self.geraHTML(self.directory, self.iteration, len(self.individuals), 1)

        return self.iteration
    
    # Pode ser melhorado, remover o individuo da lista ganha em processamento ***********************************
    def check_evacuated_individuals(self):
        for i in range(len(self.individuals)):
            if (not self.individuals[i].evacuated):
                return False
        return True
        
    def sort_individuals_by_distance(self):
        #a ordenacao eh util para que os movimentos dos individuos sejam feitas pelas distancias mais proximas
        self.individuals.sort(key = self.individual_exit_distance, reverse = False)

    def individual_exit_distance(self, individual):
        # retorna distancia da porta
        return self.static_map.map[individual.row][individual.col]


    def geraHTML(self, directory, tempoGasto, qtdIndividuos, qtdMapas):
        arquivo = open(directory+'/index.html', 'w')

        directory = ""

        arquivo.write('<!DOCTYPE HTML>\n')
        arquivo.write('<html lang="pt-br">\n')
        arquivo.write('    <head>\n')
        arquivo.write('        <meta charset="UTF-8">\n')
        arquivo.write('        <title>Relatorio Simulacao</title>\n')
        arquivo.write('        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">\n')
        arquivo.write('    </head>\n')
        arquivo.write('    <body>\n')
        arquivo.write('        <div class="container">\n')
        arquivo.write('            <div class="row">\n')
        arquivo.write('                <div class="col-md-2"></div>\n')
        arquivo.write('                    <div class="col-md-8">\n')
        arquivo.write('                        <table class="table table-striped table-hover table-condensed table-bordered table-sm">\n')
        arquivo.write('                            <thead>\n')
        arquivo.write('                                <tr>\n')
        arquivo.write('                                    <th>Indiv.</th>\n')
        arquivo.write('                                    <th>Iteracoes</th>\n')
        arquivo.write('                                    <th>#Andares</th>\n')

        arquivo.write('                                </tr>\n')
        arquivo.write('                            </thead>\n')
        arquivo.write('                        <tbody>\n')
        arquivo.write('                            <tr>\n')
        arquivo.write('                                <td>'+str(qtdIndividuos)+'</td>\n')
        arquivo.write('                                <td>'+str(tempoGasto)+'</td>\n')
        arquivo.write('                                <td>'+str(qtdMapas)+'</td>\n')

       
        arquivo.write('                            </tr>\n')
        arquivo.write('                        </tbody>\n')
        arquivo.write('                    </table>\n')
        arquivo.write('                </div>\n')
        arquivo.write('                <div class="col-md-2"></div>\n')
        arquivo.write('            </div>\n')

        #Parte para controle de javascript dos botoes
        arquivo.write('		    <div class="timers" align="center">\n')
        arquivo.write('				<button onclick="SetaMs(1)">1 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(3)">3 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(5)">5 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(10)">10 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(30)">30 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(50)">50 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(100)">100 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(300)">300 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(1000)">1000 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(3000)">3000 ms</button>\n')
        arquivo.write('				<button onclick="SetaMs(5000)">5000 ms</button>\n')
        arquivo.write('			</div>\n')
        
        arquivo.write('			<p></p>\n')
        arquivo.write('		    <div class="controls" align="center">\n')
        arquivo.write('				<button onclick="Retrocede()"> << </button>\n')
        arquivo.write('				<button onclick="Recomeca()"> PLAY </button>\n')
        arquivo.write('		    	<button onclick="Congela()"> STOP </button>\n')
        arquivo.write('		    	<button onclick="Avanca()"> >> </button>\n')
        arquivo.write('			</div>\n')




        arquivo.write('            <hr/>\n')
        arquivo.write('            <div class="row">\n')
        for i in range(qtdMapas):
            arquivo.write('                <div id="banner'+str(i)+'" class="col-md-6" align="center">\n')
            arquivo.write('                    <div id="banner_img" style="display:block">\n')
            for j in range(tempoGasto):
                arquivo.write('                        <img src="'+directory+'crowd_map/crowd_map_'+str(j)+'.png" class="img-fluid" style="display:none" id="mapa'+str(i)+"_"+str(j)+'">\n')
            arquivo.write('                    </div>\n')
            arquivo.write('                </div>\n')

        for i in range(qtdMapas):
            arquivo.write('                <div id="banner'+str(i)+'" class="col-md-6" align="center">\n')
            arquivo.write('                    <div id="banner_img" style="display:block">\n')
            for j in range(tempoGasto):
                # arquivo.write('                        <img src="imagens/Tracing'+str(i)+'_Iter'+str(j)+'.png" class="img-fluid" style="display:none" id="tracing'+str(i)+"_"+str(j)+'">\n')
                arquivo.write('                        <img src="'+directory+'dinamic_map/dinamic_map_'+str(j)+'.png" class="img-fluid" style="display:none" id="tracing'+str(i)+"_"+str(j)+'">\n')
            arquivo.write('                    </div>\n')
            arquivo.write('                </div>\n')

        for i in range(qtdMapas):
            arquivo.write('                <div id="banner'+str(i)+'" class="col-md-6" align="center">\n')
            arquivo.write('                    <div id="banner_img" style="display:block">\n')
            #static-field_Iter0
            for j in range(tempoGasto):
                iteracao = 0
                arquivo.write('                        <img src="'+directory+'cult_experiment_static-field.png" class="img-fluid" style="display:none" id="static-field'+str(i)+"_"+str(j)+'">\n')
                #arquivo.write('                        <img src="imagens/static-field_Iter'+str(iteracao)+'.png" class="img-fluid" style="display:none" id="static-field'+str(i)+"_"+str(j)+'">\n')
            arquivo.write('                    </div>\n')
            arquivo.write('                </div>\n')
        arquivo.write('            </div>\n')
        arquivo.write('            <hr/>\n')
        arquivo.write('            <div class="jumbotron" style="margin-bottom:0px">\n')
        arquivo.write('            </div>\n')
        arquivo.write('        </div>\n')
        arquivo.write('        <script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>\n')
        arquivo.write('        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>\n')
        arquivo.write('        <script>\n')

        arquivo.write('''
            function SetaMs(Timer)
            {
                clearInterval(TimeHandler)
                TimeHandler = setInterval("mudaImg()", Timer);
            }

            function Congela()
            {
                ultimoinc  = incremento
                incremento = 0
            }

            function Recomeca()
            {
                incremento = ultimoinc
            }

            function Avanca()
            {
                ultimoinc  = +1
                incremento = +1
            }

            function Retrocede()
            {
                ultimoinc  = -1
                incremento = -1
            }

            function mudaImg() {
                $('#mapa0_'+indice).css("display", "none");\n''')

        arquivo.write('''                $('#tracing0_'+indice).css("display", "none");\n''')
                
        arquivo.write('''                $('#static-field0_'+indice).css("display", "none");\n''')

        arquivo.write('''
                if (incremento > 0)
                {
                    if(indice == '''+str(tempoGasto)+''') 
                    {
                        indice = -1;
                    }
                }
                else
                {
                    if(indice == 0)
                    {
                        indice = '''+str(tempoGasto)+'''
                    }					
                }

                if(incremento != 0)
                {
                       indice = indice + incremento;
                }\n''')

        arquivo.write('''                $('#mapa0_'+indice).removeAttr("style");\n''')
        arquivo.write('''                $('#tracing0_'+indice).removeAttr("style");\n''')

        arquivo.write('''
                $('#static-field0_'+indice).removeAttr("style");
            }\n''')

        arquivo.write('''
            $(document).ready(function() {
                indice = 0;
                incremento = 1
                ultimoinc = 1
                TimeHandler = setInterval("mudaImg()", 100);
            })\n''')

        arquivo.write('        </script>\n')
        arquivo.write('    </body>\n')
        arquivo.write('</html>\n')
        arquivo.close()
