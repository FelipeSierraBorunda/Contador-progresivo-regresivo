#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include "esp_event.h"
#include "driver/gpio.h"
#include "freertos/idf_additions.h"
#include "portmacro.h"
#include "soc/gpio_num.h"
#include "soc/soc.h"
#include "hal/gpio_types.h"
#include "soc/gpio_reg.h"
#include "soc/io_mux_reg.h"
#include "soc/gpio_periph.h"

// Definición del pin a utilizar
#define PIN GPIO_NUM_16

// Función para imprimir los valores de los registros GPIO
void ImprimeRegistros() {
    uint32_t gpio_out_reg = REG_READ(GPIO_OUT_REG);
    uint32_t gpio_enable_reg = REG_READ(GPIO_ENABLE_REG);
    uint32_t gpio_func_out_sel_cfg_reg = REG_READ(GPIO_FUNC16_OUT_SEL_CFG_REG);
    uint32_t gpio_pin_reg = REG_READ(GPIO_PIN16_REG);  // Cambio aquí
    uint32_t gpio_pin_mux_reg = REG_READ(GPIO_PIN_MUX_REG[16]);  // Reemplazo GPIO_PIN_MUX_REG
    uint32_t gpio_in_reg = REG_READ(GPIO_IN_REG);
	
	
    printf("\n--- Registros GPIO ---\n");
    // Propiedades de los puertos en general (cada bit representa un puerto(en 0000 0100 el tercer bit, que representaria el puerto 3, indica que es cierto dependiendo de la condicion ))
    //Indica o controla el estado en la cual se configuraron las salidas  de los pines gpio (bit = 1  esta en alto, bit = 0 esta en bajo) (es decir, este registro depende de la programacion del puerto)
    printf("GPIO_OUT_REG: 0x%08lX\n", (unsigned long)gpio_out_reg);
        // Indica que pines estan configurados como salidas (si bit = 1, es una salida )
    printf("GPIO_ENABLE_REG: 0x%08lX\n", (unsigned long)gpio_enable_reg); 
     //Indica el estado actual de las entradas  de los pines gpio (bit = 1  esta en alto, bit = 0 esta en bajo) (es decir, lee el valor fisico de los pines, Muestra el estado real de los pines de entrada.)
    printf("GPIO_IN_REG: 0x%08lX\n", (unsigned long)gpio_in_reg);

 
    
    // Propiedades de un puerto en especifico
    // Tiene configuracion especial activa (interrupciones, wake up, funciones etc) ? Es si, si bit =1. Es no, si bit =0
    printf("GPIO_PIN15_REG: 0x%08lX\n", (unsigned long)gpio_pin_reg);
    // Este registro controla o indica lo que el Pin (en este caso 14) mandara como senal de salida
    printf("GPIO_FUNC15_OUT_SEL_CFG_REG: 0x%08lX\n", (unsigned long)gpio_func_out_sel_cfg_reg);
      // Este registro controla la multiplexación de los pines GPIO, es decir, qué función está asignada a un pin en particular.
    printf("GPIO_15_MUX_REG: 0x%08lX\n", (unsigned long)gpio_pin_mux_reg);
    
    
   
    
}

void app_main(void) {
    // Configuración del GPIO
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << PIN), 
        //Tipo de entrada 
        .mode = GPIO_MODE_INPUT_OUTPUT, 
        //Resistencias de pull up y pull down
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };

    gpio_config(&io_conf);



    // Bucle infinito con retardo
    while (true) {
		// Imprimir registros después de la configuración
       ImprimeRegistros();
       //Espera 10 ms para actualizar estado
        sleep(1000);
    }
}

