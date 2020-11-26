# Define a interface do usu�rio para o app que gera um histograma.
ui <- fluidPage(
  
  # T�tulo do app.
  titlePanel("TRANSFORMADOR DE RELAT�RIOS"),
  
  fluidRow(
    column(4)
  ),
  
  # Barra lateral com as defini��es do input e do output.
  sidebarLayout(
    
    # Barra lateral para os inputs.
    sidebarPanel(
      
      # Input: n�mero de classes do histograma.
      sliderInput(inputId = "classes",
                  label = "N�mero de classes:",
                  min = 1,
                  max = 30,
                  value = 10)
      
    ),
    
    navbarPage(
      title="Menu",
      id = "menu",
      selected = NULL,
      position = "static-top",
      inverse = TRUE,
      collapsible = TRUE,
      fluid = TRUE
    ),
    
    navbarMenu(title, ..., menuName = title, icon = NULL),
    
    # Painel principal para mostrar os outputs.
    mainPanel(
      
      # Output: Histograma
      plotOutput(outputId = "hist")
      
    )
  )
)


# Define o c�digo necess�rio para a constru��o de um histograma.
server <- function(input, output) {
  
  # Fun��o que gera o histograma e devolve para o user side.
  # Essa fun��o � reativa. Isso significa que o histograma
  # vai mudar sempre que o valor do n�mero de classes mudar.
  output$distPlot <- renderPlot({
    
    x    <- mtcars$mpg
    bins <- seq(min(x), max(x), length.out = input$classes + 1)
    
    hist(x, breaks = bins, col = "#75AADB", border = "white",
         xlab = "Milhas por gal�o",
         main = "Histograma do n�mero de milhas rodadas por gal�o de combust�vel.")
    
  })
  
}

shinyApp(ui = ui, server = server)
runApp("Tranf relat�rio", display.mode = "showcase")