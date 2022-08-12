import cv2
class WebCamCapture():
  """Classe wrapper para captura e edição de vídeo da Webcam 
     utilizando a biblitoeca "opencv-python". Criada para detecção e classificação
     de imagens em tempo real utilizando algoritmos de Aprendizagem de Máquina."""
  
  #Definição de atalhos para cores RGB
  CORES={'Preto':(0, 0, 0),'Branco':(255,255,255),'Verde':(0,255,0),'Vermelho':(0,0,255),'Azul':(255,0,0),
         'Ciano':(255, 255, 0),'Magenta':(255, 0, 255),'Amarelo':(0, 255, 255)}
  
  def __init__(self,escala=100,mostrar_info=False):
    '''Inicializa uma instância da classe WebCamCapture e um objeto VideoCapture da biblitoca opencv,
       Não inicia a captura de vídeo.
       Parâmetros:
       escala: parametro opcional que define o tamanho da imagem em porcentagem do tamanho
               da imagem orginal.: int, 100 por padrão, significando o tamanho original gerado pelo
               opencv.
       mostrar_info: bool, caso verdadeiro, a largura,altura e fps da captura aparecem no canto
                     superior direito.'''
    
    self.vidcap=cv2.VideoCapture(0)
    self.escala=escala
    self.info=mostrar_info
    self.retangulos={}
    self.textos={}
    self.font = cv2.FONT_HERSHEY_SIMPLEX
  
  def __str__(self):
    return f'WebCamCapture(escala={self.escala},mostrar_info={self.info})\n#Retângulos:{len(self.retangulos)}\n#Textos:{len(self.textos)}'
  
  def __repr__(self):
    return f'WebCamCapture(escala={self.escala},mostrar_info={self.info})'
  
  def desenhar_retangulo(self,borda1,borda2,cor,espessura=2):
    '''Método Wrapper para desenhar um retângulo na captura da Webcam.
       Parâmetros:
       borda1: (Largura,Altura) Da Borda Superior.:(int,int)
       borda2: (Largura,Altura) Da Borda Inferior.:(int,int)
       cor: Cor (R,G,B) da linha do retângulo.(int,int,int)
       espessura: Espessura da linha do retângulo :int'''
    self.retangulos[len(self.retangulos)+1]=[borda1,borda2,cor,espessura]
  
  def desenhar_texto(self,string,pos,tamanho,cor,espessura=2):
    '''Método Wrapper para desenhar um texto na captura da Webcam.
       Parâmetros:
       frame: Imagem do OpenCV
       string: Texto a ser desenhado.:str
       pos: Posição (largura,altura) do texto na captura.:(int,int)
       tamanho: Tamanho do texto:int
       cor: Cor (R,G,B) do Tetxo.(int,int,int)
       espessura: Espessura da linha do Tetxo :int'''
    self.textos[len(self.textos)+1]=[string,pos,self.font,tamanho,cor,espessura,cv2.LINE_AA]
    
    
  def comecar(self):
    '''Inicia a captura do vídeo da webcam,frame por frame e atualiza constantemente uma janela
      do sistema mostrando o frame atual, junto com os objetos adicionados à instância.
      A Janela é fechada ao apertar a tecla "ESC". '''
    
    if self.vidcap.isOpened():
        while True:
            confirmacao,frame=self.vidcap.read()
            if confirmacao:
              
                for ret in self.retangulos.values():
                  cv2.rectangle(frame,*ret)
                
                for txt in self.textos.values():
                  cv2.putText(frame,*txt)
                  
                width=self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH )
                height=self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps=self.vidcap.get(cv2.CAP_PROP_FPS)
                
                dim=(int(width*self.escala/100),int(height*self.escala/100))
                
                if self.info:
                    cv2.putText(frame,f'Largura:{dim[0]}',(500,50),
                                self.font,0.6,(0,0,0),1,cv2.LINE_AA)
                    cv2.putText(frame,f'FPS:{fps}',(500,110),
                                self.font,0.6,(0,0,0),1,cv2.LINE_AA)
                    cv2.putText(frame,f'Altura:{dim[1]}',(500,80),
                                self.font,0.6,(0,0,0),1,cv2.LINE_AA)
                if self.escala >100 or self.escala<100:
                  resized = cv2.resize(frame,dim, interpolation = cv2.INTER_AREA)
                  cv2.imshow('Webcam',resized)
                else:
                  cv2.imshow('Webcam',frame)
                c= cv2.waitKey(1)
                if c==27:
                    break
            else:
              raise ValueError('Não foi possível capturar a imagem da Webcam.')
              
        self.vidcap.release()
        cv2.destroyAllWindows()
    else:
      raise ValueError('Webcam não encontrada.')
