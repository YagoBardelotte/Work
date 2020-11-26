# Define a interface do usuário para o app que gera um histograma.
ui <- fluidPage(
  
  # Título do app.
  titlePanel("TRANSFORMADOR DE RELATÓRIOS"),
  
  fluidRow(
    column(4)
  ),
  
  # Barra lateral com as definições do input e do output.
  sidebarLayout(
    
    # Barra lateral para os inputs.
    sidebarPanel(
      
      # Input: número de classes do histograma.
      sliderInput(inputId = "classes",
                  label = "Número de classes:",
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


# Define o código necessário para a construção de um histograma.
server <- function(input, output) {
  
  # Função que gera o histograma e devolve para o user side.
  # Essa função é reativa. Isso significa que o histograma
  # vai mudar sempre que o valor do número de classes mudar.
  output$distPlot <- renderPlot({
    
    x    <- mtcars$mpg
    bins <- seq(min(x), max(x), length.out = input$classes + 1)
    
    hist(x, breaks = bins, col = "#75AADB", border = "white",
         xlab = "Milhas por galão",
         main = "Histograma do número de milhas rodadas por galão de combustível.")
    
  })
  
}

shinyApp(ui = ui, server = server)
runApp("Tranf relatório", display.mode = "showcase")